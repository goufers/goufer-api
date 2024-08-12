from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ConversationViewSet, ChatMessageViewSet

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')

# Register the ChatMessageViewSet with a nested route
conversations_router = DefaultRouter()
conversations_router.register(r'conversations/(?P<conversation_pk>\d+)/messages', ChatMessageViewSet, basename='chatmessage')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(conversations_router.urls)),  # Ensure this is included to handle nested URLs
]
