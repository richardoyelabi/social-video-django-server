# Generated by Django 4.0.7 on 2022-12-13 02:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chats', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatmessage',
            name='tip_amount',
            field=models.DecimalField(blank=True, decimal_places=50, default=0.0, max_digits=100),
        ),
        migrations.AddField(
            model_name='chatmessage',
            name='tip_currency',
            field=models.CharField(blank=True, choices=[('usd', 'United States Dollar'), ('btc', 'Bitcoin')], default='usd', max_length=3),
        ),
    ]