from django.apps import AppConfig

class Hw8Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'hw8'

    def ready(self):
        import hw8.signals

