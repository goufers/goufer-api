# Generated by Django 5.0.6 on 2024-06-25 22:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('main', '0001_initial'),
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='messageposter',
            name='custom_user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='message_poster', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='reviews',
            name='gofer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gofer_reviews', to='user.gofer'),
        ),
        migrations.AddField(
            model_name='reviews',
            name='message_poster',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_reviews', to='main.messageposter'),
        ),
        migrations.AddField(
            model_name='subcategory',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sub_categories', to='main.category'),
        ),
        migrations.AddField(
            model_name='errandboydocument',
            name='errand_boy',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='documents', to='user.errandboy'),
        ),
        migrations.AddField(
            model_name='goferdocument',
            name='gofer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='documents', to='user.gofer'),
        ),
        migrations.AddField(
            model_name='progoferdocument',
            name='pro_gofer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='documents', to='user.progofer'),
        ),
        migrations.AddField(
            model_name='vendordocument',
            name='vendor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='documents', to='user.vendor'),
        ),
    ]
