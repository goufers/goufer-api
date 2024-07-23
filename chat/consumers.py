import logging
import json
import jwt
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import ChatMessage, Conversation
from django.shortcuts import get_object_or_404
from asgiref.sync import sync_to_async
from django.conf import settings
from django.contrib.auth import get_user_model

logger = logging.getLogger(__name__)

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = None  # Initialize user to None
        query_string = self.scope['query_string'].decode()
        token = self.get_token_from_query_string(query_string)
        
        if not token:
            logger.error("Token not found in query string")
            await self.close()
            return

        self.user = await self.authenticate_user(token)
        
        if self.user is None:
            await self.close()
            return

        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'chat_{self.room_id}'

        logger.info(f"User {self.user} attempting to connect to room {self.room_id}")

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
        logger.info(f"User {self.user} connected to room {self.room_id}")

    async def disconnect(self, close_code):
        if self.user:
            logger.info(f"User {self.user} disconnecting from room {self.room_id}")
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            message = data['message']
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding JSON: {e}")
            return

        if not self.user:
            logger.error("Unauthorized user tried to send a message.")
            return

        logger.info(f"Message received from user {self.user}: {message}")

        room = await self.get_room(self.room_id)
        if not room:
            logger.warning(f"Room {self.room_id} not found")
            return

        await self.save_message(room, self.user, message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': self.user.username,
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender': event['sender'],
        }))

    @sync_to_async
    def get_room(self, room_id):
        return get_object_or_404(Conversation, id=room_id)

    @sync_to_async
    def save_message(self, room, user, message):
        ChatMessage.objects.create(
            room=room,
            sender=user,
            content=message
        )

    @sync_to_async
    def authenticate_user(self, token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user = get_user_model().objects.get(id=payload['user_id'])
            return user
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, get_user_model().DoesNotExist) as e:
            logger.error(f"Authentication error: {e}")
            return None

    def get_token_from_query_string(self, query_string):
        try:
            return query_string.split('=')[1]
        except IndexError:
            return None