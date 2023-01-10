# Generated by Django 4.0.7 on 2022-12-29 14:54

from django.db import migrations

from django.contrib.sites.models import Site
from django.conf import settings

def set_domain_info(apps, schema_editor):
    SiteModel = apps.get_model("sites", "Site")
    SiteModel.objects.get_or_create(
        domain = settings.SITE_DOMAIN,
        name = settings.SITE_DISPLAY
    )

class Migration(migrations.Migration):

    dependencies = [
        ("sites", "0002_alter_domain_unique"),
    ]

    operations = [
        migrations.RunPython(set_domain_info)
    ]