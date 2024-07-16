import logging
import logging
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import Conversation, ChatMessage
from .serializers import ConversationSerializer, ChatMessageSerializer
from user.models import Gofer, Vendor, ProGofer, ErrandBoy
from main.models import MessagePoster

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['POST'], permission_classes=[IsAuthenticated])
    @action(detail=False, methods=['POST'], permission_classes=[IsAuthenticated])
    def create_chat_room(self, request):
        user = request.user
        gofer_id = request.data.get('gofer_id')
        vendor_id = request.data.get('vendor_id')
        progofer_id = request.data.get('progofer_id')
        errand_boy_id = request.data.get('errand_boy_id')

        '''Ensure only one participant is specified'''
        participant_count = sum([bool(gofer_id), bool(vendor_id), bool(progofer_id), bool(errand_boy_id)])
        if participant_count != 1:
            return Response({'error': 'Exactly one participant (gofer, vendor,errandboy or progofer) must be specified'}, status=status.HTTP_400_BAD_REQUEST)

        # Validate and create conversation based on the participant type
        if gofer_id:
            gofer = get_object_or_404(Gofer, id=gofer_id)
            # Check if there's an existing conversation between the user and the gofer
            existing_conversation = Conversation.objects.filter(Q(message_poster=user, gofer=gofer) | Q(message_poster=gofer, gofer=user)).first()
            if existing_conversation:
                return Response({'message': 'Chat room already exists', 'room_id': existing_conversation.id}, status=status.HTTP_200_OK)
            # Create new conversation
            conversation = Conversation.objects.create(message_poster=user, gofer=gofer)
            return Response({'message': 'Chat room created', 'room_id': conversation.id}, status=status.HTTP_201_CREATED)

        elif vendor_id:
            vendor = get_object_or_404(Vendor, id=vendor_id)
            gofer = user.gofer  # Assuming user has a one-to-one relation with Gofer
            # Check if there's an existing conversation between the user's gofer and the vendor
            existing_conversation = Conversation.objects.filter(gofer=gofer, vendor=vendor).first()
            if existing_conversation:
                return Response({'message': 'Chat room already exists', 'room_id': existing_conversation.id}, status=status.HTTP_200_OK)
            # Create new conversation
            conversation = Conversation.objects.create(message_poster=user, gofer=gofer, vendor=vendor)
            return Response({'message': 'Chat room created', 'room_id': conversation.id}, status=status.HTTP_201_CREATED)

        elif progofer_id:
            progofer = get_object_or_404(ProGofer, id=progofer_id)
            # Check if there's an existing conversation between the user and the progofer
            existing_conversation = Conversation.objects.filter(Q(message_poster=user, progofer=progofer) | Q(message_poster=progofer, progofer=user)).first()
            if existing_conversation:
                return Response({'message': 'Chat room already exists', 'room_id': existing_conversation.id}, status=status.HTTP_200_OK)
            # Create new conversation
            conversation = Conversation.objects.create(message_poster=user, progofer=progofer)
            return Response({'message': 'Chat room created', 'room_id': conversation.id}, status=status.HTTP_201_CREATED)
        
        elif errand_boy_id:
            errand_boy = get_object_or_404(ProGofer, id=errand_boy_id)
            # Check if there's an existing conversation between the user and the errand boy
            existing_conversation = Conversation.objects.filter(Q(message_poster=user, errand_boy=errand_boy) | Q(message_poster=errand_boy, errand_boy=user)).first()
            if existing_conversation:
                return Response({'message': 'Chat room already exists', 'room_id': existing_conversation.id}, status=status.HTTP_200_OK)
            # Create new conversation
            conversation = Conversation.objects.create(message_poster=user, errand_boy=errand_boy)
            return Response({'message': 'Chat room created', 'room_id': conversation.id}, status=status.HTTP_201_CREATED)

        else:
            return Response({'error': 'Invalid parameters'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['GET'], permission_classes=[IsAuthenticated])
    @action(detail=True, methods=['GET'], permission_classes=[IsAuthenticated])
    def chat_room(self, request, pk=None):
        chat_room = self.get_object()
        serializer = self.get_serializer(chat_room)
        return Response(serializer.data)

logger = logging.getLogger(__name__)
logger = logging.getLogger(__name__)
class ChatMessageViewSet(viewsets.ModelViewSet):
    queryset = ChatMessage.objects.all()
    serializer_class = ChatMessageSerializer
    permission_classes = [IsAuthenticated]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        room_id = self.kwargs['conversation_pk']
        return ChatMessage.objects.filter(room_id=room_id)

    def perform_create(self, serializer):
        room_id = self.kwargs['conversation_pk']
        conversation = get_object_or_404(Conversation, pk=room_id)
        logger.info(f"Saving message for room {room_id} and conversation {conversation.id}")
        logger.info(f"Saving message for room {room_id} and conversation {conversation.id}")
        serializer.save(room=conversation, sender=self.request.user)
