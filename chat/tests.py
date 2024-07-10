from django.test import TestCase
from django.contrib.auth import get_user_model
from user.models import CustomUser, Gofer, Vendor, ProGofer
from main.models import MessagePoster
from .models import Conversation, ChatMessage
from .serializers import ConversationSerializer, ChatMessageSerializer
from .views import ConversationViewSet, ChatMessageViewSet
from channels.testing import WebsocketCommunicator
from django.conf import settings
from django.urls import reverse
from rest_framework.test import APIClient
import jwt
from goufer.asgi import application

User = get_user_model()

class ChatAppTests(TestCase):
    def setUp(self):
        sub_category_id = 1  # Replace with an actual sub_category_id that exists in your database
        self.user1 = User.objects.create_user(email='moshood@gmail.com', password='go2work22', phone_number="+2348039958684")
        self.user2 = User.objects.create_user(email='lanre@gmail.com', password='go2work22', phone_number="+2349029958684")
        self.message_poster = MessagePoster.objects.create(custom_user=self.user1)
        self.gofer = Gofer.objects.create(
            custom_user=self.user2,
            expertise='Some expertise',
            mobility_means='Motorcycle',
            sub_category_id=sub_category_id,  # Provide a valid sub_category_id
            charges=0,
            is_available=True,
            avg_rating=0
        )

        self.conversation = Conversation.objects.create(
            message_poster=self.message_poster,
            gofer=self.gofer,
        )
        
        self.chat_message = ChatMessage.objects.create(
            room=self.conversation,
            sender=self.user1,
            content='Hello!'
        )

    # Your other test methods remain unchanged


    # def test_conversation_creation(self):
    #     self.assertEqual(self.conversation.message_poster, self.message_poster)
    #     self.assertEqual(self.conversation.gofer, self.gofer)
    #     self.assertTrue(self.conversation.is_open)

    # def test_chat_message_creation(self):
    #     self.assertEqual(self.chat_message.room, self.conversation)
    #     self.assertEqual(self.chat_message.sender, self.user1)
    #     self.assertEqual(self.chat_message.content, 'Hello!')

    # def test_conversation_serializer(self):
    #     serializer = ConversationSerializer(instance=self.conversation)
    #     data = serializer.data
    #     self.assertEqual(data['message_poster'], self.message_poster.id)
    #     self.assertEqual(data['gofer'], self.gofer.id)
    #     self.assertTrue(data['is_open'])

    # def test_chat_message_serializer(self):
    #     serializer = ChatMessageSerializer(instance=self.chat_message)
    #     data = serializer.data
    #     self.assertEqual(data['room'], self.conversation.id)
    #     self.assertEqual(data['sender'], self.user1.id)
    #     self.assertEqual(data['content'], 'Hello!')

    # async def test_websocket_connect_and_send_message(self):
    #     token = jwt.encode({'user_id': self.user1.id}, settings.SECRET_KEY, algorithm='HS256')
    #     communicator = WebsocketCommunicator(application, f'/ws/api/v1/chat/conversation/{self.conversation.id}/', headers={'Authorization': f'Bearer {token.decode()}'})
    #     connected, subprotocol = await communicator.connect()
    #     self.assertTrue(connected)

    #     await communicator.send_json_to({
    #         'message': 'Hello from user1'
    #     })

    #     response = await communicator.receive_json_from()
    #     self.assertEqual(response['message'], 'Hello from user1')
    #     self.assertEqual(response['sender'], self.user1.username)

    #     await communicator.disconnect()

    # async def test_websocket_authentication_failure(self):
    #     communicator = WebsocketCommunicator(application, f'/ws/api/v1/chat/conversation/{self.conversation.id}/')
    #     connected, subprotocol = await communicator.connect()
    #     self.assertFalse(connected)

    # async def test_websocket_receive_message(self):
    #     token = jwt.encode({'user_id': self.user1.id}, settings.SECRET_KEY, algorithm='HS256')
    #     communicator = WebsocketCommunicator(application, f'/ws/api/v1/chat/conversation/{self.conversation.id}/', headers={'Authorization': f'Bearer {token.decode()}'})
    #     await communicator.connect()

    #     await communicator.send_json_to({
    #         'message': 'Hello from user1'
    #     })

    #     response = await communicator.receive_json_from()
    #     self.assertEqual(response['message'], 'Hello from user1')
    #     self.assertEqual(response['sender'], self.user1.username)

    #     await communicator.disconnect()

    # def test_api_endpoints(self):
    #     client = APIClient()

    #     # Test ConversationViewSet endpoints
    #     url = reverse('conversation-list')
    #     response = client.get(url)
    #     self.assertEqual(response.status_code, 200)

    #     # Test ChatMessageViewSet endpoints
    #     url = reverse('conversation-messages-list', kwargs={'conversation_lookup': self.conversation.id})
    #     response = client.get(url)
    #     self.assertEqual(response.status_code, 200)