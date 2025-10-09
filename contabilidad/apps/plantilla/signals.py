from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.apps import apps

@receiver(post_migrate)
def ejecutar_seeders(sender, **kwargs):
    if sender.name != "contabilidad.apps.plantilla":  # Solo correr para tu app específica
        return

    try:
        from contabilidad.apps.plantilla.seeds import seed_permiso
        seed_permiso.run()
        print("✅ Seeders ejecutados correctamente después de migrate")
    except Exception as e:
        print(f"❌ Error ejecutando seeders: {e}")
