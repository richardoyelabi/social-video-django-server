# Generated by Django 4.0.7 on 2022-12-09 10:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('public_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('time_of_transaction', models.DateTimeField(auto_now_add=True)),
                ('transaction_currency', models.CharField(choices=[('usd', 'United States Dollar'), ('btc', 'Bitcoin')], max_length=3)),
                ('amount_sent', models.DecimalField(decimal_places=50, default=0.0, max_digits=100)),
                ('platform_fee', models.DecimalField(decimal_places=50, default=0.0, max_digits=100)),
                ('amount_received', models.DecimalField(decimal_places=50, default=0.0, max_digits=100)),
                ('transaction_type', models.CharField(choices=[('deposit', 'Deposit'), ('withdraw', 'Withdrawal'), ('subscribe', 'Subscription payment'), ('buy', 'Video purchase'), ('tip', 'Creator tip'), ('request', 'Special request payment')], max_length=10)),
                ('record_is_balanced', models.BooleanField(default=False)),
                ('receiver', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='credit_transactions', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='debit_transactions', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
