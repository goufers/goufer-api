# Generated by Django 5.0.6 on 2024-06-20 10:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_alter_contract_custom_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contract',
            name='custom_user',
        ),
    ]
