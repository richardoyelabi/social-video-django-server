# Generated by Django 4.0.7 on 2022-12-13 18:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_account_notification_seen'),
    ]

    operations = [
        migrations.RenameField(
            model_name='account',
            old_name='site_notification',
            new_name='site_promotion',
        ),
    ]