from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from django.db.models import F, Q
from .models import Conversation, ChatMessage
from .serializers import ConversationSerializer, ChatMessageSerializer
from user.models import Gofer, CustomUser

class ChatRoomListCreate(generics.ListCreateAPIView):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    #permission_classes = [permissions.IsAuthenticated]
 
class ChatRoomDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    #permission_classes = [permissions.IsAuthenticated]

class ChatMessageListCreate(generics.ListCreateAPIView):
    queryset = ChatMessage.objects.all()
    serializer_class = ChatMessageSerializer
    #permission_classes = [permissions.IsAuthenticated]

class ChatMessageDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ChatMessage.objects.all()
    serializer_class = ChatMessageSerializer
    #permission_classes = [permissions.IsAuthenticated]

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def gofers_list(request):
    user = request.user
    gofers = Gofer.objects.annotate(order=F('id'))
    users = CustomUser.objects.all()

    try:
        gofer = Gofer.objects.get(user=user.id)
        chat_rooms = Conversation.objects.filter(Q(user=user) | Q(gofer=gofer))
    except Gofer.DoesNotExist:
        chat_rooms = Conversation.objects.filter(user=user)

    return Response({
        'gofers': gofers.values(),
        'users': users.values(),
        'chat_rooms': chat_rooms.values()
    })

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_chat_room(request, gofer_id):
    user = request.user
    gofer = get_object_or_404(Gofer, id=gofer_id)

    # Debug logging
    print(f"Attempting to create chat room for user: {user.username} (ID: {user.id}), gofer: {gofer.name} (ID: {gofer.id})")

    # Check for existing chat rooms before creating
    existing_chat_rooms = Conversation.objects.filter(user=user, gofer=gofer)
    print(f"Found {existing_chat_rooms.count()} existing chat rooms for user: {user.id}, gofer: {gofer.id}")

    if existing_chat_rooms.exists():
        chat_room = existing_chat_rooms.first()
        
        return Response({'message': 'Chat room already exists', 'room_id': chat_room.id}, status=status.HTTP_200_OK)

    # Create new chat room if it doesn't exist
    chat_room = Conversation.objects.create(user=user, gofer=gofer)
    print(f"Chat room created with ID: {chat_room.id}")
    return Response({'message': 'Chat room created', 'room_id': chat_room.id}, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def chat_room(request, room_id):
    chat_room = get_object_or_404(Conversation, id=room_id)
    return Response(ConversationSerializer(chat_room).data)
