# Generated by Django 4.0.7 on 2022-10-12 23:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video_purchases', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cancelledpurchase',
            name='fee_amount',
            field=models.DecimalField(decimal_places=50, default=0.0, max_digits=100),
        ),
        migrations.AddField(
            model_name='cancelledpurchase',
            name='fee_currency',
            field=models.CharField(choices=[('usd', 'United States Dollar'), ('btc', 'Bitcoin')], default='usd', max_length=3),
        ),
        migrations.AddField(
            model_name='nullifiedpurchase',
            name='fee_amount',
            field=models.DecimalField(decimal_places=50, default=0.0, max_digits=100),
        ),
        migrations.AddField(
            model_name='nullifiedpurchase',
            name='fee_currency',
            field=models.CharField(choices=[('usd', 'United States Dollar'), ('btc', 'Bitcoin')], default='usd', max_length=3),
        ),
        migrations.AddField(
            model_name='purchase',
            name='fee_amount',
            field=models.DecimalField(decimal_places=50, default=0.0, max_digits=100),
        ),
        migrations.AddField(
            model_name='purchase',
            name='fee_currency',
            field=models.CharField(choices=[('usd', 'United States Dollar'), ('btc', 'Bitcoin')], default='usd', max_length=3),
        ),
    ]
