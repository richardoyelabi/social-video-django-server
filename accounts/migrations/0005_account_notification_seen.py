# Generated by Django 4.0.7 on 2022-12-13 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_account_connected_account_email_message_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='notification_seen',
            field=models.BooleanField(default=True),
        ),
    ]