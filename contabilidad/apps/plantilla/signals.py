from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.core.management import call_command

@receiver(post_migrate)
def ejecutar_seeders(sender, **kwargs):
    if sender.name != "contabilidad.apps.plantilla":
        return

    try:
        print("▶ Ejecutando comando seed_all después de migrate...")
        call_command("seed_all")
        print("✅ Seed_all ejecutado correctamente después de migrate")
    except Exception as e:
        print(f"❌ Error ejecutando seed_all: {e}")
