from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter
from .views import ConversationViewSet, ChatMessageViewSet

# Create the main router
router = DefaultRouter()
router.register(r'conversation', ConversationViewSet, basename='conversation')

# Create a nested router
conversation_router = NestedDefaultRouter(router, r'conversation', lookup='conversation')
conversation_router.register(r'messages', ChatMessageViewSet, basename='conversation-messages')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(conversation_router.urls)),
    
    
    
]
