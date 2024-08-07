from django.contrib import admin
from .models import ChatMessage, Conversation, ProgoferAcceptance


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'content', 'room_id', 'edited', 'timestamp']
    search_fields = ['sender', 'content']
    list_filter = ['sender', 'content']
admin.site.register(Conversation)
admin.site.register(ProgoferAcceptance)
