# Generated by Django 4.0.7 on 2022-10-01 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_alter_account_btc_wallet_balance_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='notification_settings',
            field=models.JSONField(blank=True, null=True),
        ),
    ]