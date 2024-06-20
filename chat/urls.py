from django.urls import path
from .views import ChatRoomListCreate, ChatRoomDetail,  gofers_list, create_chat_room, chat_room
# ChatMessageListCreate, ChatMessageDetail,
urlpatterns = [
    # New API endpoints
    path('chat-rooms/', ChatRoomListCreate.as_view(), name='chat_room_list_create'),
    #path('chat-rooms/<int:pk>/', ChatRoomDetail.as_view(), name='chat_room_detail'),
    # path('chat-messages/', ChatMessageListCreate.as_view(), name='chat_message_list_create'),
    # path('chat-messages/<int:pk>/', ChatMessageDetail.as_view(), name='chat_message_detail'),
    
    # Existing views converted to API
    path('create-chat-room/<int:gofer_id>/', create_chat_room, name='create_chat_room'),
    #path('chat-room/<int:room_id>/', chat_room, name='chat_room'),
    path('gofers_list/', gofers_list, name='gofers_list'),
]
