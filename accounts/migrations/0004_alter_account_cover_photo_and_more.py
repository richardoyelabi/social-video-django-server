# Generated by Django 4.0.7 on 2022-10-07 17:26

from django.db import migrations
import versatileimagefield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_account_cover_photo_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='cover_photo',
            field=versatileimagefield.fields.VersatileImageField(blank=True, null=True, upload_to='cover_photos/<django.db.models.query_utils.DeferredAttribute object at 0x7fc9f4de9ab0>'),
        ),
        migrations.AlterField(
            model_name='account',
            name='profile_photo',
            field=versatileimagefield.fields.VersatileImageField(blank=True, null=True, upload_to='profile_photos/<django.db.models.query_utils.DeferredAttribute object at 0x7fc9f4de9ab0>'),
        ),
    ]
