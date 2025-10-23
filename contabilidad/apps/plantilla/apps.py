from django.apps import AppConfig


class PlantillaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'contabilidad.apps.plantilla'

    def ready(self):
        import contabilidad.apps.plantilla.signals