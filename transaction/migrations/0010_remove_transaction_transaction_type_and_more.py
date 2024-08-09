# Generated by Django 5.0.7 on 2024-08-07 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0009_alter_stripeuser_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='transaction_type',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='wallet',
        ),
        migrations.AddField(
            model_name='transaction',
            name='payment_id',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
