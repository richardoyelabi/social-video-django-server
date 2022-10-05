# Generated by Django 4.0.7 on 2022-10-05 18:22

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='subscriptions',
            field=models.ManyToManyField(related_name='subscribers', through='subscriptions.Subscription', to=settings.AUTH_USER_MODEL),
        ),
    ]