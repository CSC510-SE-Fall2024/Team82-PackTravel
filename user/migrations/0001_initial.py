# Generated by Django 5.1.2 on 2024-11-14 01:47
# user/migrations/0001_initial.py
"""
Initial migration for creating the Profile model with fields like phone_number,
travel_preferences, likes, and is_smoker, associated with the User model.
"""
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(blank=True, max_length=15)),
                ('travel_preferences', models.CharField(blank=True, max_length=255)),
                ('likes', models.CharField(blank=True, max_length=255)),
                ('is_smoker', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
