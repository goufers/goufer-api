# Generated by Django 5.0.6 on 2024-07-23 03:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='conversation',
            name='payment_status',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='conversation',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
