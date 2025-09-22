from django.core.management.base import BaseCommand
from ...models.usuario import User, Persona

class Command(BaseCommand):
    help = "Crea 5 usuarios de prueba junto con sus personas"

    def handle(self, *args, **kwargs):
        for i in range(1, 6):
            username = f"user{i}"
            email = f"user{i}@example.com"

            if not User.objects.filter(username=username).exists():
                # Crear persona primero
                persona = Persona.objects.create(
                    nombre=f"Nombre{i}",
                    apellido=f"Apellido{i}",
                    ci=f"CI{i:05d}",
                    telefono=f"700000{i}"
                )

                # Crear usuario asociado
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password="password123",
                    persona=persona
                )

                self.stdout.write(self.style.SUCCESS(f"✅ Usuario creado: {user.username}"))
            else:
                self.stdout.write(self.style.WARNING(f"⚠️ Usuario {username} ya existe"))
