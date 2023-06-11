from django.apps import AppConfig


class SpecialRequestsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "special_requests"

    def ready(self):
        import special_requests.signals
