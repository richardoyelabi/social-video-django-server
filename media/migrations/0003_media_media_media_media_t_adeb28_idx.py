# Generated by Django 4.0.7 on 2022-12-13 02:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0002_media'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='media',
            index=models.Index(fields=['media_type', 'media_id'], name='media_media_media_t_adeb28_idx'),
        ),
    ]
