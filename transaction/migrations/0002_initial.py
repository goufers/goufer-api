# Generated by Django 5.0.6 on 2024-06-14 16:58

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
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='transfer_recipient', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='schedule',
            name='day',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='transaction.day'),
        ),
        migrations.AddField(
            model_name='schedule',
            name='from_hour',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_hour', to='transaction.hour'),
        ),
        migrations.AddField(
            model_name='schedule',
            name='gofer_or_errandBoy',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='active_schedules', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='schedule',
            name='to_hour',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_hour', to='transaction.hour'),
        ),
        migrations.AddField(
            model_name='schedule',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='schedules', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='wallet',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wallet', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='transaction',
            name='wallet',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='transaction.wallet'),
        ),
        migrations.AddConstraint(
            model_name='schedule',
            constraint=models.UniqueConstraint(fields=('user', 'gofer_or_errandBoy', 'day', 'from_hour', 'to_hour'), name='unique_schedule'),
        ),
    ]
