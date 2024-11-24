# Generated by Django 4.1.2 on 2024-11-22 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_notification'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='user',
        ),
        migrations.AddField(
            model_name='notification',
            name='username',
            field=models.CharField(default='Anonymous', max_length=255),
        ),
    ]