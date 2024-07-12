from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from user.models import CustomUser, Gofer
from chat.models import ChatRoom

class ChatAPITestCase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', email='testuser@example.com', password='testpassword')
        self.gofer_user = CustomUser.objects.create_user(username='goferuser', email='goferuser@example.com', password='goferpassword')
        self.gofer = Gofer.objects.create(user=self.gofer_user)
        self.client.login(username='testuser', password='testpassword')

    def test_create_chat_room(self):
        url = reverse('create_chat_room', args=[self.gofer.id])
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('room_id', response.data)

        # Attempt to create the same chat room again
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('room_id', response.data)
        self.assertEqual(response.data['message'], 'Chat room already exists')

        # Check the total number of chat rooms to ensure only one was created
        chat_rooms = ChatRoom.objects.filter(user=self.user, gofer=self.gofer)
        self.assertEqual(chat_rooms.count(), 1)