# Generated by Django 4.0.7 on 2022-12-23 09:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("transactions", "0004_alter_transaction_transaction_type"),
    ]

    operations = [
        migrations.AddField(
            model_name="withdrawalrequest",
            name="timestamp",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name="Withdrawal",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "public_id",
                    models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
                ),
                (
                    "wallet",
                    models.CharField(
                        choices=[("usd", "United States Dollar"), ("btc", "Bitcoin")],
                        default="usd",
                        max_length=3,
                    ),
                ),
                (
                    "amount",
                    models.DecimalField(decimal_places=50, default=0.0, max_digits=100),
                ),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
                (
                    "creator",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="withdrawals",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
