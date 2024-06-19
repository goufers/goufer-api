from rest_framework import generics, permissions
from .models import ChatRoom, ChatMessage
from .serializers import ChatRoomSerializer, ChatMessageSerializer
from user.models import Gofer, CustomUser
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from django.db.models import F, Q
from rest_framework import status

class ChatRoomListCreate(generics.ListCreateAPIView):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer
    #permission_classes = [permissions.IsAuthenticated]

class ChatRoomDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer
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
#@permission_classes([permissions.IsAuthenticated])
def gofers_list(request):
    gofers = Gofer.objects.annotate(order=F('id'))
    users = CustomUser.objects.all()
    user = request.user

    try:
        gofer = Gofer.objects.get(user=user.id)
        chat_rooms = ChatRoom.objects.filter(Q(user=user) | Q(gofer=gofer))
    except Gofer.DoesNotExist:
        chat_rooms = ChatRoom.objects.filter(user=user)
    
    return Response({
        'gofers': gofers.values(),
        'users': users.values(),
        'chat_rooms': chat_rooms.values()
    })

@api_view(['POST'])
#@permission_classes([permissions.IsAuthenticated])
def create_chat_room(request, gofer_id):
    user = request.user
    gofer = get_object_or_404(Gofer, id=gofer_id)
    print(f"Creating chat room for user: {user.username}, gofer: {gofer.name}")
    chat_room, created = ChatRoom.objects.get_or_create(user=user, gofer=gofer)
    if created:
        print(f"Chat room created: {chat_room.id}")
        return Response({'message': 'Chat room created', 'room_id': chat_room.id}, status=status.HTTP_201_CREATED)
    else:
        print(f"Chat room already exists: {chat_room.id}")
        return Response({'message': 'Chat room already exists', 'room_id': chat_room.id}, status=status.HTTP_200_OK)

@api_view(['GET'])
#@permission_classes([permissions.IsAuthenticated])
def chat_room(request, room_id):
    chat_room = get_object_or_404(ChatRoom, id=room_id)
    return Response(ChatRoomSerializer(chat_room).data)