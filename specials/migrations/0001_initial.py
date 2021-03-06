# Generated by Django 3.0.2 on 2020-02-12 09:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import specials.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.UUIDField(default=specials.models.hex_uuid, editable=False, primary_key=True, serialize=False, unique=True)),
                ('category_name', models.CharField(max_length=50)),
                ('description', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.UUIDField(default=specials.models.hex_uuid, editable=False, primary_key=True, serialize=False, unique=True)),
                ('store_name', models.CharField(max_length=30)),
                ('description', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.UUIDField(default=specials.models.hex_uuid, editable=False, primary_key=True, serialize=False, unique=True)),
                ('deal_title', models.CharField(max_length=250)),
                ('slug', models.SlugField(max_length=500, unique=True)),
                ('deal_url', models.URLField(blank=True, max_length=250, null=True, unique=True)),
                ('description', models.TextField()),
                ('price', models.PositiveIntegerField()),
                ('original_price', models.PositiveIntegerField(blank=True, null=True)),
                ('discount', models.DecimalField(blank=True, decimal_places=2, max_digits=100, null=True)),
                ('brand', models.CharField(blank=True, max_length=250, null=True)),
                ('front_page', models.BooleanField(blank=True, default=False, null=True)),
                ('src', models.ImageField(upload_to='images/items')),
                ('published_at', models.DateTimeField(auto_now_add=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category', to='specials.Category')),
                ('store', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='store', to='specials.Store')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-published_at'],
            },
        ),
    ]
