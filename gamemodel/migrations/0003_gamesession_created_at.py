# Generated by Django 5.1.4 on 2024-12-14 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gamemodel', '0002_remove_gamesession_created_at_gamesession_history_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='gamesession',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
