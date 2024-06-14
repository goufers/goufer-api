# Generated by Django 5.0.6 on 2024-06-14 16:58

import django.core.validators
import main.validate
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(choices=[('food', 'Food'), ('entertainment', 'Entertainment'), ('transportation', 'Transportation'), ('tourism_and_travel', 'Tourism & Travel'), ('religious_donations', 'Religious Donations'), ('medical', 'Medical'), ('services', 'Services'), ('legal', 'Legal'), ('technical', 'Technical'), ('employments', 'Employment'), ('housing', 'Housing'), ('shopping', 'Shopping')], max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contract_code', models.CharField(max_length=10, unique=True)),
                ('contract_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('pay_rate', models.DecimalField(decimal_places=2, max_digits=10)),
                ('contract_length', models.IntegerField()),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('days_remaining', models.IntegerField(default=0)),
                ('contract_status', models.CharField(choices=[('Pending', 'Pending'), ('Active', 'Active'), ('Settled', 'Settled'), ('Declined', 'Declined'), ('Terminated', 'Terminated')], default='Pending', max_length=20)),
                ('remark', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document_type', models.CharField(choices=[('bvn', 'BVN'), ('nin', 'NIN')], max_length=5)),
                ('document_number', models.CharField(max_length=11)),
                ('document_of_expertise', models.FileField(upload_to='main/documents', validators=[main.validate.validate_file_size, django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'png', 'pdf'])])),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('is_verified', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.FloatField(blank=True, null=True)),
                ('longitude', models.FloatField(blank=True, null=True)),
                ('address', models.CharField(max_length=200)),
                ('state', models.CharField(max_length=50)),
                ('country', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Reviews',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(blank=True, null=True)),
                ('rating', models.DecimalField(decimal_places=2, default=0.0, max_digits=3)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
    ]
