# Generated by Django 4.0.7 on 2023-01-11 23:26

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("transactions", "0005_withdrawalrequest_timestamp_withdrawal"),
    ]

    operations = [
        migrations.AlterField(
            model_name="transaction",
            name="transaction_type",
            field=models.CharField(
                choices=[
                    ("deposit", "Deposit"),
                    ("withdraw", "Withdrawal"),
                    ("subscribe", "Subscription payment"),
                    ("buy", "Video purchase"),
                    ("tip", "Creator tip"),
                    ("request", "Special request payment"),
                ],
                max_length=10,
            ),
        ),
    ]