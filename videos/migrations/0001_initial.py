# Generated by Django 4.0.7 on 2022-10-10 15:20

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('public_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('content_type', models.CharField(choices=[('paid_post', 'Premium post'), ('paid_chat', 'Premium message'), ('free_post', 'Free post'), ('free_chat', 'Free Message')], max_length=10)),
                ('upload_time', models.DateTimeField(auto_now=True)),
                ('video', models.FileField(upload_to='videos/%Y/%m/%d', validators=[django.core.validators.FileExtensionValidator(['mp4'])])),
                ('uploader', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='video_uploads', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
