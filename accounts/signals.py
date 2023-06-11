from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.conf import settings

from .models import CreatorInfo


# Create a CreatorInfo model for each new instance of AUTH_USER_MODEL when is_creator is true
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_creator_info(sender, instance, created, **kwargs):
    if created:
        if instance.is_creator:
            CreatorInfo.objects.create(creator=instance)
