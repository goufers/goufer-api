# Generated by Django 5.0.6 on 2024-06-26 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0003_alter_schedule_pro_gofer_schedule_unique_schedule'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedule',
            name='maximum_bookings',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='booking',
            name='status',
            field=models.CharField(choices=[('Active', 'Active'), ('Terminated', 'Terminated'), ('Settled', 'Settled'), ('Pending Approval', 'Pending Approval'), ('Declined', 'Declined'), ('Cancelled', 'Cancelled')], default='Pending Approval', max_length=20),
        ),
    ]
