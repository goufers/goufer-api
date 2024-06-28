# Generated by Django 5.0.6 on 2024-06-25 10:35

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('chat', '0001_initial'),
        ('user', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='chatmessage',
            name='sender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_messages', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='conversation',
            name='gofer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chats', to='user.gofer'),
        ),
        migrations.AddField(
            model_name='conversation',
            name='message_poster',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chat_rooms', to='user.messageposter'),
        ),
        migrations.AddField(
            model_name='chatmessage',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='chat.conversation'),
        ),
    ]
