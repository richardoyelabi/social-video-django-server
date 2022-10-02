# Generated by Django 4.0.7 on 2022-10-02 10:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('subscriptions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cancelledsubscription',
            name='subscribed_to',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cancelled_sub_subscribed_to_set', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='cancelledsubscription',
            name='subscriber',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cancelled_sub_subscriber_set', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='nullifiedsubscription',
            name='subscribed_to',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='nullified_sub_subscribed_to_set', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='nullifiedsubscription',
            name='subscriber',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='nullified_sub_subscriber_set', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='subscribed_to',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subs_subscribed_to_set', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='subscriber',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sub_subscriber_set', to=settings.AUTH_USER_MODEL),
        ),
    ]