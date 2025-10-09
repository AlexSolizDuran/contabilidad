from django.apps import AppConfig


class ConfigurarConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'contabilidad.apps.empresa'
    def ready(self):
        import contabilidad.apps.empresa.signals
        