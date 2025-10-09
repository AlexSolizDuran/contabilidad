from django.db.models.signals import post_save
from django.dispatch import receiver
from ..plantilla.models import PlantillaClase
from ..gestion_cuenta.models import ClaseCuenta
from .models import Empresa

@receiver(post_save, sender=Empresa)
def crear_clases_por_defecto(sender, instance, created, **kwargs):
    if created:
        # Primero, crear un diccionario temporal para mapear plantillas a clases
        plantilla_a_cuenta = {}

        # Obtenemos todas las plantillas ordenadas por código
        for plantilla in PlantillaClase.objects.all().order_by('codigo'):
            # Obtenemos el padre si existe
            padre = None
            if plantilla.padre:
                padre = plantilla_a_cuenta.get(plantilla.padre.id)

            # Creamos la clase en la empresa
            cuenta = ClaseCuenta.objects.create(
                empresa=instance,
                nombre=plantilla.nombre,
                codigo=plantilla.codigo,
                padre=padre
            )

            # Guardamos la relación temporal
            plantilla_a_cuenta[plantilla.id] = cuenta
