# chat/consumers.py

from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .models import ChatMessage, ChatRoom
from django.shortcuts import get_object_or_404
from asgiref.sync import sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'chat_{self.room_id}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        
        # Get authenticated user from scope
        user = self.scope['user']

        # Save message to database
        await self.save_message_to_db(user, message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': user.username,  # Use username as sender for simplicity
            }
        )

    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']

        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender,
        }))

    async def save_message_to_db(self, user, message):
        room = await self.get_room(self.room_id)
        if room:
            await self.save_message(room, user, message)

    @sync_to_async
    def get_room(self, room_id):
        return get_object_or_404(ChatRoom, id=room_id)

    @sync_to_async
    def save_message(self, room, user, message):
        ChatMessage.objects.create(
            room=room,
            sender=user,  # Assign the authenticated user instance
            content=message
        )