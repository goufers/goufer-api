from django.db import models
    

''' CHAT MODELS '''
class ChatRoom(models.Model):
    user = models.ForeignKey("CustomUser", related_name='user_rooms', on_delete=models.CASCADE)
    gofer = models.ForeignKey("Gofer", related_name='chats', on_delete=models.CASCADE)
    is_open = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self) -> str:
        return f"Chat between {self.user.username} and {self.gofer.user.username}"

class ChatMessage(models.Model):
    room = models.ForeignKey(ChatRoom, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey("CustomUser", related_name='sent_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self) -> str:
        return f"Sent Message from {self.sender.username}"
