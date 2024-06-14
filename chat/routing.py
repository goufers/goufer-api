# chat/routing.py
from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
     re_path(r'ws/api/v1/chat/chat-room/(?P<room_id>\d+)/$', consumers.ChatConsumer.as_asgi()),
]