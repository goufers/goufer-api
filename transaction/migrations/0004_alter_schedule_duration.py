# Generated by Django 5.0.6 on 2024-06-12 19:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0003_alter_bank_recipient_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='duration',
            field=models.IntegerField(null=True, verbose_name='Duration (optional)'),
        ),
    ]