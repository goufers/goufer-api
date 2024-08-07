if gofer_id:
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
                return Response({'message': 'A new chat room is created', 
                                 "room_id": conversation.id,
                                 'room_id': existing_conversation.id, 
                                 'room_name': str(existing_conversation), 
                                 'sender': user.first_name}, 
                                status=status.HTTP_201_CREATED)

            else:
                conversation = Conversation.objects.create(message_poster=message_poster, gofer=gofer, is_open=True)
                return Response({'message': 'Chat room created', 
                                 "id": conversation.id,
                                 'room_id': existing_conversation.id, 
                                 'room_name': str(existing_conversation), 
                                 'sender': user.first_name}, 
                                status=status.HTTP_201_CREATED)