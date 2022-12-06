# Generated by Django 4.0.7 on 2022-12-06 08:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_of_subscription', models.DateTimeField(auto_now_add=True)),
                ('fee_currency', models.CharField(choices=[('usd', 'United States Dollar'), ('btc', 'Bitcoin')], default='usd', max_length=3)),
                ('fee_amount', models.DecimalField(decimal_places=50, default=0.0, max_digits=100)),
                ('subscribed_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subs_subscribed_to_set', to=settings.AUTH_USER_MODEL)),
                ('subscriber', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sub_subscriber_set', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='NullifiedSubscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_of_nullification', models.DateTimeField(auto_now_add=True)),
                ('time_of_initial_subscription', models.DateTimeField()),
                ('fee_currency', models.CharField(choices=[('usd', 'United States Dollar'), ('btc', 'Bitcoin')], default='usd', max_length=3)),
                ('fee_amount', models.DecimalField(decimal_places=50, default=0.0, max_digits=100)),
                ('subscribed_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='nullified_sub_subscribed_to_set', to=settings.AUTH_USER_MODEL)),
                ('subscriber', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='nullified_sub_subscriber_set', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CancelledSubscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_of_cancellation', models.DateTimeField(auto_now_add=True)),
                ('time_of_initial_subscription', models.DateTimeField()),
                ('fee_currency', models.CharField(choices=[('usd', 'United States Dollar'), ('btc', 'Bitcoin')], default='usd', max_length=3)),
                ('fee_amount', models.DecimalField(decimal_places=50, default=0.0, max_digits=100)),
                ('subscribed_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cancelled_sub_subscribed_to_set', to=settings.AUTH_USER_MODEL)),
                ('subscriber', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cancelled_sub_subscriber_set', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
