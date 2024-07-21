# Generated by Django 5.0.6 on 2024-07-17 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_alter_reviews_message_poster_delete_messageposter'),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expatriate_name', models.CharField(max_length=100)),
                ('date', models.DateField()),
                ('purpose', models.TextField()),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('declined', 'Declined')], default='pending', max_length=10)),
            ],
        ),
    ]