from django.urls import path
from .views import ChatRoomListCreate, ChatRoomDetail, ChatMessageListCreate, ChatMessageDetail, gofers_list, create_chat_room, chat_room

urlpatterns = [
    # New API endpoints
    path('api/chat-rooms/', ChatRoomListCreate.as_view(), name='chat_room_list_create'),
    path('api/chat-rooms/<int:pk>/', ChatRoomDetail.as_view(), name='chat_room_detail'),
    path('api/chat-messages/', ChatMessageListCreate.as_view(), name='chat_message_list_create'),
    path('api/chat-messages/<int:pk>/', ChatMessageDetail.as_view(), name='chat_message_detail'),
    
    # Existing views converted to API
    path('create-chat-room/<int:gofer_id>/', create_chat_room, name='create_chat_room'),
    path('chat-room/<int:room_id>/', chat_room, name='chat_room'),
    path('gofers_list/', gofers_list, name='gofers_list'),
]
