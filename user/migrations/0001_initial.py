# Generated by Django 5.0.6 on 2024-06-14 16:58

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('username', models.CharField(blank=True, max_length=255, null=True)),
                ('email', models.EmailField(db_index=True, max_length=254, unique=True)),
                ('phone_number', models.CharField(db_index=True, max_length=30, unique=True)),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to='files/dp')),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Others')], default='M', max_length=1)),
                ('phone_verified', models.BooleanField(default=False)),
                ('email_verified', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, related_name='user_groups', to='auth.group')),
                ('location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.location')),
                ('user_permissions', models.ManyToManyField(blank=True, related_name='user_user_permissions', to='auth.permission')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ErrandBoy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mobility_means', models.CharField(choices=[('Bicycle', 'Bicycle'), ('Motorcycle', 'Motorcycle'), ('Car', 'Car'), ('Truck', 'Truck'), ('Van', 'Van'), ('Bus', 'Bus'), ('Other', 'Other')], default='Bicycle', max_length=20)),
                ('charges', models.IntegerField(default=0)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='errand_boy', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Gofer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expertise', models.CharField(default=None, max_length=200)),
                ('mobility_means', models.CharField(choices=[('Bicycle', 'Bicycle'), ('Motorcycle', 'Motorcycle'), ('Car', 'Car'), ('Truck', 'Truck'), ('Van', 'Van'), ('Bus', 'Bus'), ('Other', 'Other')], default='Motorcycle', max_length=20)),
                ('bio', models.TextField(max_length=1024)),
                ('charges', models.IntegerField(default=0)),
                ('is_on_contract', models.BooleanField(default=False)),
                ('custom_user', models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='gofer', to=settings.AUTH_USER_MODEL)),
                ('sub_category', models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, related_name='gofers', to='main.subcategory')),
            ],
        ),
        migrations.CreateModel(
            name='Errand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_description', models.TextField()),
                ('estimated_duration', models.IntegerField(blank=True, null=True)),
                ('status', models.CharField(choices=[('Completed', 'Completed'), ('Ongoing', 'Ongoing'), ('Terminated', 'Terminated')], default='O', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('sub_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.subcategory')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='errands_sent', to=settings.AUTH_USER_MODEL)),
                ('gofer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='errands', to='user.gofer')),
            ],
        ),
        migrations.CreateModel(
            name='Availability',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('days_of_week', models.JSONField()),
                ('is_available', models.BooleanField(default=True)),
                ('gofer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='availability', to='user.gofer')),
            ],
        ),
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('business_name', models.CharField(max_length=255)),
                ('website', models.URLField(blank=True, null=True)),
                ('bio', models.TextField(blank=True, null=True)),
                ('facebook', models.URLField(blank=True, null=True)),
                ('twitter', models.URLField(blank=True, null=True)),
                ('instagram', models.URLField(blank=True, null=True)),
                ('linkedin', models.URLField(blank=True, null=True)),
                ('category', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='vendor_category', to='main.category')),
                ('custom_user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='vendor', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
