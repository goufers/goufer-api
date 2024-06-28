# Generated by Django 5.0.6 on 2024-06-25 22:46

import django.core.validators
import django.db.models.deletion
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
                ('category_name', models.CharField(choices=[('food', 'Food'), ('entertainment', 'Entertainment'), ('transportation', 'Transportation'), ('tourism_and_travel', 'Tourism & Travel'), ('religious_donations', 'Religious Donations'), ('medical', 'Medical'), ('services', 'Services'), ('legal', 'Legal'), ('technical', 'Technical'), ('employments', 'Employment'), ('housing', 'Housing'), ('real_estate', 'Real Estate')], max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='GoferDocument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document_type', models.CharField(choices=[('ssn', 'SSN'), ('nin', 'NIN')], max_length=5)),
                ('document_number', models.CharField(max_length=11, unique=True)),
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
            name='MessagePoster',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
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
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='ErrandBoyDocument',
            fields=[
                ('document_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='main.document')),
            ],
            bases=('main.document',),
        ),
        migrations.CreateModel(
            name='GoferDocument',
            fields=[
                ('document_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='main.document')),
                ('document_of_expertise', models.FileField(upload_to='main/documents', validators=[main.validate.validate_file_size, django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'png', 'pdf'])])),
            ],
            bases=('main.document',),
        ),
        migrations.CreateModel(
            name='ProGoferDocument',
            fields=[
                ('document_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='main.document')),
                ('document_of_expertise', models.FileField(upload_to='main/documents/pro_gofer', validators=[main.validate.validate_file_size, django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'png', 'pdf'])])),
            ],
            bases=('main.document',),
        ),
        migrations.CreateModel(
            name='VendorDocument',
            fields=[
                ('document_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='main.document')),
                ('document_of_expertise', models.FileField(upload_to='main/documents', validators=[main.validate.validate_file_size, django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'png', 'pdf'])])),
            ],
            bases=('main.document',),
        ),
    ]
