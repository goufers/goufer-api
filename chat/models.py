from django.db import models
from user.models import CustomUser, Gofer, Vendor, ProGofer
from main.models import MessagePoster   
from user.models import CustomUser, Gofer, Vendor, ProGofer, ErrandBoy
from main.models import MessagePoster   

''' CHAT MODELS '''
class ProgoferAcceptance(models.Model):    
    payment_status = models.BooleanField(default=False)
    payment_accepted = models.BooleanField(default=False)
    message_poster = models.ForeignKey(MessagePoster, related_name='progofer_acceptance', on_delete=models.CASCADE, null=True, blank=True)
    progofer = models.ForeignKey(ProGofer, related_name='progofer_acceptance', on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return f"Acceptance for {self.message_poster}"
class Conversation(models.Model):
    message_poster = models.ForeignKey(MessagePoster, related_name='chat_rooms', on_delete=models.CASCADE, null=True, blank=True)
    gofer = models.ForeignKey(Gofer, related_name='chats', on_delete=models.CASCADE, null=True, blank=True)
    vendor = models.ForeignKey(Vendor, related_name='chats', on_delete=models.CASCADE, null=True, blank=True)
    progofer = models.ForeignKey(ProGofer, related_name='chats', on_delete=models.CASCADE, null=True, blank=True)
    errand_boy=models.ForeignKey(ErrandBoy, related_name='chats', on_delete=models.CASCADE, null=True, blank=True)
    progofer_acceptance = models.ForeignKey(ProgoferAcceptance, related_name=
                                            'acceptance', on_delete=models.CASCADE, null=True, blank=True)    
    is_open = models.BooleanField(default=True, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self) -> str:
        participants = []
        if self.message_poster:
            participants.append(f"User {self.message_poster.custom_user.first_name}")
        if self.gofer:
            participants.append(f"Gofer {self.gofer.custom_user.first_name}")
        if self.vendor:
            participants.append(f"Vendor {self.vendor.custom_user.first_name}")
        if self.progofer:
            participants.append(f"ProGofer {self.progofer.custom_user.first_name}")
        if self.errand_boy:
            participants.append(f"ErandBoy {self.errand_boy.user.first_name}")
        return f"Chat between {' and '.join(participants)}"

class ChatMessage(models.Model):
    room = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(CustomUser, related_name='sent_messages', on_delete=models.CASCADE)
    
    content = models.TextField()
    attachment = models.FileField(upload_to='chat_attachments/', blank=True, null=True)
    reply_to = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='replies')
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)
    
    
    
    def __str__(self) -> str:
        return f"Sent Message from {self.sender.first_name} at room_id {self.room.id} in message_id {self.id}"


    
    
    
        
