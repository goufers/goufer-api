# Generated by Django 5.0.6 on 2024-06-25 11:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_remove_reviews_user_reviews_message_poster_and_more'),
        ('user', '0004_remove_gofer_is_on_contract'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='location',
        ),
        migrations.AddField(
            model_name='gofer',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.location'),
        ),
    ]
