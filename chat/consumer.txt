import logging
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import ChatMessage, Conversation
from django.shortcuts import get_object_or_404
from asgiref.sync import sync_to_async

logger = logging.getLogger(__name__)

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'chat_{self.room_id}'

        logger.info(f"User {self.scope['user']} attempting to connect to room {self.room_id}")

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
        logger.info(f"User {self.scope['user']} connected to room {self.room_id}")

    async def disconnect(self, close_code):
        logger.info(f"User {self.scope['user']} disconnecting from room {self.room_id}")
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

        user = self.scope['user']
        logger.info(f"Message received from user {user}: {message}")

        room = await self.get_room(self.room_id)
        if not room:
            logger.warning(f"Room {self.room_id} not found")
            return

        await self.save_message(room, user, message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': user.username,
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
