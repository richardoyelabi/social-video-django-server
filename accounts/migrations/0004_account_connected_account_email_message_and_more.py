# Generated by Django 4.0.7 on 2022-12-12 15:10

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0003_alter_creatorinfo_identity"),
    ]

    operations = [
        migrations.AddField(
            model_name="account",
            name="connected",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="account",
            name="email_message",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="account",
            name="email_promotion",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="account",
            name="site_message",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="account",
            name="site_notification",
            field=models.BooleanField(default=True),
        ),
    ]
