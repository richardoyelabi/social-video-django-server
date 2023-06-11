from django.apps import AppConfig


class VideoPurchasesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "video_purchases"

    def ready(self):
        import video_purchases.signals
