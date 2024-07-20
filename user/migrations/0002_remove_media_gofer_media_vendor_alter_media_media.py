# Generated by Django 5.0.6 on 2024-07-12 19:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='media',
            name='gofer',
        ),
        migrations.AddField(
            model_name='media',
            name='vendor',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='vendor_media', to='user.vendor'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='media',
            name='media',
            field=models.ImageField(upload_to='media/vendors/media'),
        ),
    ]
