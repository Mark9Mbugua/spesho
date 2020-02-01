# Generated by Django 3.0.2 on 2020-02-01 08:56

import accounts.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('id', models.UUIDField(default=accounts.models.hex_uuid, editable=False, primary_key=True, serialize=False, unique=True)),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('first_name', models.CharField(blank=True, max_length=20, null=True)),
                ('last_name', models.CharField(blank=True, max_length=20, null=True)),
                ('verified', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=False)),
                ('staff', models.BooleanField(default=False)),
                ('admin', models.BooleanField(default=False)),
                ('published_on', models.DateTimeField(auto_now_add=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.UUIDField(default=accounts.models.hex_uuid, editable=False, primary_key=True, serialize=False)),
                ('bio', models.TextField(blank=True, null=True)),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='users/profile')),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None)),
                ('gender', models.CharField(blank=True, choices=[('Male', 'Male'), ('Female', 'Female'), ('Others', 'Others')], max_length=6, null=True)),
                ('published_date', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateField(auto_now=True)),
                ('verification_code', models.CharField(blank=True, max_length=6, null=True)),
                ('confirmed_code', models.BooleanField(blank=True, default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
