from django.db import models
from user.models import CustomUser, Gofer, MessagePoster    

''' CHAT MODELS '''
class Conversation(models.Model):
    message_poster = models.ForeignKey(MessagePoster, related_name='chat_rooms', on_delete=models.CASCADE)
    gofer = models.ForeignKey(Gofer, related_name='chats', on_delete=models.CASCADE)
    is_open = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self) -> str:
        return f"Chat between User {self.message_poster.custom_username.first_name} and Gofer {self.gofer.custom_user.first_name}"

class ChatMessage(models.Model):
    room = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(CustomUser, related_name='sent_messages', on_delete=models.CASCADE)
    content = models.TextField()
    attachment = models.FileField(upload_to='chat_attachments/', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self) -> str:
        return f"Sent Message from {self.sender.username} at room_id {self.room.id}"
