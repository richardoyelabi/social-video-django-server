# Generated by Django 4.0.7 on 2022-10-29 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_post_posts_post_media_t_7b364b_idx'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='comments_number',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='post',
            name='likes_number',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
