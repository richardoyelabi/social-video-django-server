# Generated by Django 4.0.7 on 2022-12-10 08:50

from django.db import migrations
import versatileimagefield.fields


class Migration(migrations.Migration):
    dependencies = [
        ("verifications", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="idupload",
            name="upload",
            field=versatileimagefield.fields.VersatileImageField(
                upload_to="id_uploads"
            ),
        ),
    ]
