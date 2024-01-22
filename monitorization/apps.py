from django.apps import AppConfig



class MonitorizationConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "monitorization"

    
    def ready(self) -> None:
        import monitorization.utils.signals