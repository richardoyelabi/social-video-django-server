# Generated by Django 4.0.7 on 2022-12-06 08:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('chats', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Tip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('fee_currency', models.CharField(choices=[('usd', 'United States Dollar'), ('btc', 'Bitcoin')], default='usd', max_length=3)),
                ('fee_amount', models.DecimalField(decimal_places=50, default=0.0, max_digits=100)),
                ('receiver', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='received_tips', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sent_tips', to=settings.AUTH_USER_MODEL)),
                ('tip_message', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='chats.chatmessage')),
            ],
        ),
    ]
