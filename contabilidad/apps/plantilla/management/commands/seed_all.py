# plantilla/management/commands/seed_all.py
from django.core.management.base import BaseCommand
from ...seeds import (
    seed_permiso,seed_custom,seed_plantilla_clase,seed_user,seed_plantilla_rol
)

class Command(BaseCommand):
    help = "Ejecuta todos los seeders del módulo plantilla en orden definido"

    def handle(self, *args, **kwargs):
        orden_seeders = [
            seed_user,seed_permiso,seed_custom,seed_plantilla_clase,seed_plantilla_rol
        ]

        for seeder in orden_seeders:
            self.stdout.write(self.style.NOTICE(f"➡️ Ejecutando {seeder.__name__}..."))
            try:
                seeder.run()
                self.stdout.write(self.style.SUCCESS(f"✅ {seeder.__name__} ejecutado correctamente"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"❌ Error ejecutando {seeder.__name__}: {e}"))
                break

        self.stdout.write(self.style.SUCCESS("🌱 Todos los seeders ejecutados correctamente"))
