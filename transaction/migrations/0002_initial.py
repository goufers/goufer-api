# Generated by Django 5.1 on 2024-08-12 15:34

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('transaction', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='bank',
            name='custom_user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='transfer_recipient', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='stripeuser',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='stripe_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='wallet',
            name='custom_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wallet', to=settings.AUTH_USER_MODEL),
        ),
    ]
