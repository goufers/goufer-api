# chat/test/test_url.py

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from user.models import CustomUser, Gofer, Vendor, ProGofer, ErrandBoy
from chat.models import Conversation, ChatMessage
from main.models import MessagePoster, Category, SubCategory

class ChatAPITestCase(APITestCase):
    def setUp(self):
        # Create users for authentication
        self.user = CustomUser.objects.create_user(email='testuser@example.com', password='testpassword', phone_number='1234567890')
        self.gofer_user_custom = CustomUser.objects.create_user(email='goferuser@example.com', password='testpassword', phone_number='0987654321')

        # Create a category
        self.category = Category.objects.create(category_name='TestCategory')
        
        # Create a sub-category
        self.subcategory = SubCategory.objects.create(name='TestSubCategory', category=self.category)

        # Create instances for different user types
        self.gofer_user = Gofer.objects.create(custom_user=self.gofer_user_custom, expertise='Cleaning', sub_category=self.subcategory)
        self.vendor_user = Vendor.objects.create(custom_user=self.user, category=self.category)
        self.progofer = ProGofer.objects.create(custom_user=self.user, hourly_rate=50.00)
        self.errand_boy_user = ErrandBoy.objects.create(user=self.user)

        # Initialize APIClient for making requests
        self.client = APIClient()

        # Obtain JWT token for the user
        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)
        
        # Include the JWT token in the request headers
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

        # Create sample message posters
        self.message_poster = MessagePoster.objects.create(custom_user=self.user)
        self.gofer_message_poster = MessagePoster.objects.create(custom_user=self.gofer_user.custom_user)

        # Create sample conversations
        self.conversation = Conversation.objects.create(message_poster=self.message_poster, is_open=True)
        self.gofer_conversation = Conversation.objects.create(message_poster=self.gofer_message_poster, gofer=self.gofer_user, is_open=True)

    def test_conversation_list(self):
        # Test the conversation list endpoint
        url = reverse('conversation-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Assuming there are two conversations

    def test_conversation_detail(self):
        # Test the conversation detail endpoint
        url = reverse('conversation-detail', args=[self.conversation.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Adjust the assertion to check specific fields in response.data
        self.assertEqual(response.data['id'], self.conversation.id)
        self.assertEqual(response.data['is_open'], self.conversation.is_open)
        
        # Check if the message poster's name is in the response (adjust as per your model structure)
        self.assertIn(self.message_poster.custom_user.first_name, str(response.data))
    
    def test_create_chat_message(self):
        url = reverse('conversation-messages-list', args=[self.conversation.id])
        data = {
            'content': 'Hello, world!',
            'room': self.conversation.id,
            'sender': self.user.id,
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ChatMessage.objects.count(), 1)
        self.assertEqual(ChatMessage.objects.get().content, 'Hello, world!')
    
    def test_chat_message_list(self):
        # Create a sample chat message
        chat_message = ChatMessage.objects.create(room=self.conversation, sender=self.user, content='Test Message')

        # Test the chat message list endpoint
        url = reverse('conversation-messages-list', args=[self.conversation.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['content'], 'Test Message')
