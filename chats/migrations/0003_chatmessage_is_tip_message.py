# Generated by Django 4.0.7 on 2022-11-25 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chats', '0002_alter_chatmessage_media_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatmessage',
            name='is_tip_message',
            field=models.BooleanField(default=False),
        ),
    ]