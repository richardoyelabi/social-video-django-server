# Generated by Django 4.0.7 on 2022-11-26 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0027_account_unique_post_views'),
    ]

    operations = [
        migrations.AddField(
            model_name='creatorinfo',
            name='feed_score',
            field=models.FloatField(default=1),
        ),
    ]
