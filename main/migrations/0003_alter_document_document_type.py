# Generated by Django 5.0.6 on 2024-06-14 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='document_type',
            field=models.CharField(choices=[('ssn', 'SSN'), ('nin', 'NIN')], max_length=5),
        ),
    ]