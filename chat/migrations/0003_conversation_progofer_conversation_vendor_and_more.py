# Generated by Django 5.0.6 on 2024-07-04 04:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_initial'),
        ('main', '0002_initial'),
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='conversation',
            name='progofer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='chats', to='user.progofer'),
        ),
        migrations.AddField(
            model_name='conversation',
            name='vendor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='chats', to='user.vendor'),
        ),
        migrations.AlterField(
            model_name='conversation',
            name='gofer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='chats', to='user.gofer'),
        ),
        migrations.AlterField(
            model_name='conversation',
            name='message_poster',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='chat_rooms', to='main.messageposter'),
        ),
    ]
