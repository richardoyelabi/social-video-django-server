from django.apps import AppConfig


class VideoSavesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "video_saves"

    def ready(self):
        import video_saves.signals
