from django.apps import AppConfig


class FlightConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Flight'

    def ready(self):
        # Ensure signals are loaded
        import Flight.signals