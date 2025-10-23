from django.db.models.signals import post_save
from django.dispatch import receiver
from ..plantilla.models import PlantillaClase,PlantillaRol
from ..gestion_cuenta.models import ClaseCuenta
from .models import Empresa,RolEmpresa,Permiso

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

@receiver(post_save, sender=Empresa)
def crear_rol_por_defecto(sender, instance, created, **kwargs):
    if created:
        plantilla_rol = {}

        # Definición de permisos por tipo de rol
        permisos_contador = [
            "ver_cuenta", "crear_cuenta", "editar_cuenta", "eliminar_cuenta",
            "ver_asiento", "crear_asiento", "editar_asiento", "eliminar_asiento",
            "ver_movimiento","ver_libro_diario", "ver_libro_mayor",
            "ver_balancel_general","ver_estado_resultado","ver_clase_cuenta"
        ]

        permisos_auxiliar = [
            "ver_cuenta", "crear_cuenta",
            "ver_clase_cuenta", 
            "ver_asiento", "crear_asiento",
            "ver_movimiento",
            "ver_libro_diario", "ver_libro_mayor",
            "ver_balancel_general","ver_estado_resultado",
        ]

        permisos_auditor = [
            "ver_cuenta", "ver_clase_cuenta", "ver_asiento",
            "ver_movimiento", "ver_libro_diario", "ver_libro_mayor",
            "ver_balancel_general","ver_estado_resultado",
        ]

        for plantilla in PlantillaRol.objects.all():
            rol = RolEmpresa.objects.create(
                empresa=instance,
                nombre=plantilla.nombre,
            )

            nombre_rol = plantilla.nombre.lower()

            # 🔹 Administrador → todos los permisos
            if nombre_rol == "admin":
                rol.permisos.set(Permiso.objects.all())

            # 🔹 Contador
            elif nombre_rol == "contador":
                rol.permisos.set(Permiso.objects.filter(nombre__in=permisos_contador))

            # 🔹 Auxiliar contable
            elif nombre_rol in ["auxiliar contable", "auxiliar_contable"]:
                rol.permisos.set(Permiso.objects.filter(nombre__in=permisos_auxiliar))

            # 🔹 Auditor
            elif nombre_rol == "auditor":
                rol.permisos.set(Permiso.objects.filter(nombre__in=permisos_auditor))

            plantilla_rol[plantilla.id] = rol