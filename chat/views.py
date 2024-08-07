import logging
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import Conversation, ChatMessage, ProgoferAcceptance
from .serializers import ConversationSerializer, ChatMessageSerializer
from user.models import Gofer, Vendor, ProGofer, ErrandBoy, MessagePoster, CustomUser

logger = logging.getLogger(__name__)

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['POST'], permission_classes=[IsAuthenticated])
    def create_chat_room(self, request):
        user = request.user
        gofer_id = request.data.get('gofer') or None
        vendor_id = request.data.get('vendor') or None
        progofer_id = request.data.get('progofer') or None
        errand_boy_id = request.data.get('errand_boy') or None
        
    
        
        '''Ensure only one participant is specified'''
        participant_ids = [gofer_id, vendor_id, progofer_id, errand_boy_id]

        count = 0
        for participant_id in participant_ids:
            if participant_id != "":
                count += 1
        
        if count == 0:    
            return Response({'error': 'Exactly one participant (gofer, vendor, errandboy, or progofer) must be specified'}, status=status.HTTP_400_BAD_REQUEST)

        '''Validate and create conversation based on the participant type'''
        
        '''Create chat room between a message poster and a gofer'''
        if progofer_id:
            message_poster =  get_object_or_404(MessagePoster, custom_user = user )
            print("################################")
            print("message poster below")
            print(message_poster)
            progofer = get_object_or_404(ProGofer, id=progofer_id)
            print("################################")
            print("progofer below")
            print(progofer)
            
            progofer_acceptance = ProgoferAcceptance.objects.filter(message_poster=message_poster, progofer=progofer).first()
            existing_conversation_3 = Conversation.objects.filter(message_poster=message_poster, progofer=progofer).last()
            
            if progofer_acceptance is not None and progofer_acceptance.payment_accepted == True and progofer_acceptance.payment_status ==True and existing_conversation_3 is not None and  existing_conversation_3.is_open == True:
                return Response ({'message': 'This chat room already exist.', 
                                 'room_id': existing_conversation_3.id,
                                 'room_name': str(existing_conversation_3),
                                 'sender': user.first_name,
                                 'payment status': progofer_acceptance.payment_status,
                                 'payment_accepted_by_progofer': progofer_acceptance.payment_accepted}, 
                                status=status.HTTP_200_OK)
            
            elif progofer_acceptance is not None and progofer_acceptance.payment_accepted == True and progofer_acceptance.payment_status ==True and existing_conversation_3 is None:
                conversation = Conversation.objects.create(message_poster=message_poster, progofer=progofer, is_open=True)
                return Response ({'message': 'A new chat room is created', 
                                 'room_id': conversation.id,
                                 'room_name': str(existing_conversation_3),
                                 'sender': user.first_name,
                                 'payment status': progofer_acceptance.payment_status,
                                 'payment_accepted_by_progofer': progofer_acceptance.payment_accepted}, 
                                status=status.HTTP_200_OK)
            
            
            elif progofer_acceptance is not None and progofer_acceptance.payment_accepted == True and progofer_acceptance.payment_status ==True and existing_conversation_3 is not None and existing_conversation_3.is_open == False:
                conversation = Conversation.objects.create(message_poster=message_poster, progofer=progofer, is_open=True)
                return Response ({'message': 'A fresh chat room has been created. Previous chat room is closed.', 
                                 'room_id': conversation.id,
                                 'room_name': str(existing_conversation_3),
                                 'sender': user.first_name,
                                 'payment status': progofer_acceptance.payment_status,
                                 'payment_accepted_by_progofer': progofer_acceptance.payment_accepted}, 
                                status=status.HTTP_200_OK)
            
            
            
            
            
            
            
            else:
                
                return Response({'message': 'No room created.', 
                                  'sender': user.first_name,
                                  'payment status': progofer_acceptance.payment_status,
                                  'payment_accepted_by_progofer': progofer_acceptance.payment_accepted},
                                status=status.HTTP_402_PAYMENT_REQUIRED)
                
        
        elif vendor_id is not None and gofer_id is not None:
            vendor = get_object_or_404(Vendor, id=vendor_id)
            print(vendor)
           
            '''User has one to one relationship with gofer'''
            gofer = get_object_or_404(Gofer, id=gofer_id)
            print(gofer)
            
            
            existing_conversation_2 = Conversation.objects.filter(gofer=gofer, vendor=vendor).last()
            if existing_conversation_2 is not None and existing_conversation_2.is_open == True:
                return Response({'message': 'This chat room already exists', 
                                 'room_id': existing_conversation_2.id,
                                 'room_name': str(existing_conversation_2),
                                 'sender': user.first_name}, 
                                status=status.HTTP_200_OK)
                
            elif existing_conversation_2 is not None and existing_conversation_2.is_open == False:
                conversation = Conversation.objects.create(gofer=gofer, vendor=vendor, is_open=True)
                return Response({"message": 'Another new chat room created. Previous chat room(s) closed',
                                 'room_id': conversation.id,
                                 'room_name': str(existing_conversation_2),
                                 'sender': user.first_name},
                                 status=status.HTTP_201_CREATED)
            
            else:   
                conversation = Conversation.objects.create(gofer=gofer, vendor=vendor)
                return Response({'message': 'A new chat room has been created', 
                                 'room_id': conversation.id,
                                 'room_name': str(existing_conversation_2),
                                 'sender': user.first_name}, 
                                status=status.HTTP_201_CREATED)
        
        elif gofer_id is not None:
            gofer = get_object_or_404(Gofer, id=gofer_id)
            message_poster = get_object_or_404(MessagePoster, custom_user = user )
            
            
            existing_conversation = Conversation.objects.filter(message_poster=message_poster, gofer=gofer).last()
            
            
            
            
            
            
            if existing_conversation is not None and existing_conversation.is_open == True:
                return Response({'message': 'This chat room already exists.', 
                                 'room_id': existing_conversation.id, 
                                 'room_name': str(existing_conversation), 
                                 'sender': user.first_name }, 
                                status=status.HTTP_200_OK) 
            
            elif existing_conversation is not None and existing_conversation.is_open == False:
                conversation = Conversation.objects.create(message_poster=message_poster, gofer=gofer, is_open=True)
                return Response({'message': 'A new chat room is created, previously chat room closed.', 
                                 'room_id': conversation.id, 
                                 'room_name': str(existing_conversation), 
                                 'sender': user.first_name}, 
                                status=status.HTTP_201_CREATED)

            else:
                conversation = Conversation.objects.create(message_poster=message_poster, gofer=gofer, is_open=True)
                return Response({'message': 'Chat room created',                                 
                                 'room_id': conversation.id, 
                                 'room_name': str(existing_conversation), 
                                 'sender': user.first_name}, 
                                status=status.HTTP_201_CREATED)
        
        elif errand_boy_id is not None:
            errand_boy = get_object_or_404(ErrandBoy, id=errand_boy_id)
            message_poster = get_object_or_404(MessagePoster, custom_user = user )
            
            
            existing_conversation_4 = Conversation.objects.filter(message_poster=message_poster, errand_boy=errand_boy).last()
            
            
            
            
            
            
            if existing_conversation_4 is not None and existing_conversation_4.is_open == True:
                return Response({'message': 'This chat room already exists.', 
                                 'room_id': existing_conversation_4.id, 
                                 'room_name': str(existing_conversation_4), 
                                 'sender': user.first_name }, 
                                status=status.HTTP_200_OK) 
            
            elif existing_conversation_4 is not None and existing_conversation_4.is_open == False:
                conversation = Conversation.objects.create(message_poster=message_poster, errand_boy=errand_boy, is_open=True)
                return Response({'message': 'A new fresh chat room is created, previous chat room closed successfully', 
                                 'room_id': existing_conversation_4.id, 
                                 'room_name': str(existing_conversation_4), 
                                 'sender': user.first_name}, 
                                status=status.HTTP_201_CREATED)

            else:
                conversation = Conversation.objects.create(message_poster=message_poster, errand_boy=errand_boy, is_open=True)
                return Response({'message': 'A new  fresh chat room is created.',                                
                                 'room_id': conversation.id, 
                                 'room_name': str(existing_conversation_4), 
                                 'sender': user.first_name}, 
                                status=status.HTTP_201_CREATED)
            
        

        # elif errand_boy_id:
        #     errand_boy = get_object_or_404(ErrandBoy, id=errand_boy_id)
        #     existing_conversation = Conversation.objects.filter(Q(message_poster=user, errand_boy=errand_boy) | Q(message_poster=errand_boy, errand_boy=user)).first()
        #     if existing_conversation:
        #         return Response({'message': 'Chat room already exists', 'room_id': existing_conversation.id}, status=status.HTTP_200_OK)
        #     conversation = Conversation.objects.create(message_poster=user, errand_boy=errand_boy)
        #     return Response({'message': 'Chat room created', 'room_id': conversation.id}, status=status.HTTP_201_CREATED)

        else:
            return Response({'error': 'Invalid parameters'}, status=status.HTTP_400_BAD_REQUEST)

class ChatMessageViewSet(viewsets.ModelViewSet):
    queryset = ChatMessage.objects.all()
    serializer_class = ChatMessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        room_id = self.kwargs['conversation_pk']
        queryset = ChatMessage.objects.filter(room_id=room_id)

        # Prefetch replies for nesting
        queryset = queryset.prefetch_related('replies')

        return queryset

    def perform_create(self, serializer):
        room_id = self.kwargs['conversation_pk']
        conversation = get_object_or_404(Conversation, pk=room_id)
        reply_to_message = None
        reply_to_id = self.request.data.get('reply_to')

        if reply_to_id:
            reply_to_message = get_object_or_404(ChatMessage, id=reply_to_id, room=conversation)

        # Save the message with its reply relationship
        serializer.save(room=conversation, sender=self.request.user, reply_to=reply_to_message)

    def perform_update(self, serializer):
        # Mark the message as edited
        serializer.instance.edited = True
        serializer.save()