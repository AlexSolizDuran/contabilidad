# plantilla/seeds/seed_permisos_custom.py
from ...empresa.models import Permiso

def run():
    permisos_data = [
    # Cuentas
    {"nombre": "ver_cuenta", "descripcion": "Puede ver cuentas"},
    {"nombre": "crear_cuenta", "descripcion": "Puede crear cuentas"},
    {"nombre": "editar_cuenta", "descripcion": "Puede editar cuentas"},
    {"nombre": "eliminar_cuenta", "descripcion": "Puede eliminar cuentas"},
    # ClaseCuenta
    {"nombre": "ver_clase_cuenta", "descripcion": "Puede ver clases de cuenta"},
    {"nombre": "crear_clase_cuenta", "descripcion": "Puede crear clases de cuenta"},
    {"nombre": "editar_clase_cuenta", "descripcion": "Puede editar clases de cuenta"},
    {"nombre": "eliminar_clase_cuenta", "descripcion": "Puede eliminar clases de cuenta"},
    # Asientos
    {"nombre": "ver_asiento", "descripcion": "Puede ver asientos"},
    {"nombre": "crear_asiento", "descripcion": "Puede crear asientos"},
    {"nombre": "editar_asiento", "descripcion": "Puede editar asientos"},
    {"nombre": "eliminar_asiento", "descripcion": "Puede eliminar asientos"},
    # Movimientos
    {"nombre": "ver_movimiento", "descripcion": "Puede ver movimientos"},
    # Rol
    {"nombre": "ver_rol", "descripcion": "Puede ver roles"},
    {"nombre": "crear_rol", "descripcion": "Puede crear roles"},
    {"nombre": "editar_rol", "descripcion": "Puede editar roles"},
    {"nombre": "eliminar_rol", "descripcion": "Puede eliminar roles"},
    # Permiso
    {"nombre": "asignar_rol", "descripcion": "Puede asignar roles"},
    {"nombre": "asginar_permiso", "descripcion": "Puede asignar permisos"},
    # Colaborador
    {"nombre": "ver_colaborador", "descripcion": "Puede ver colaboradores"},
    {"nombre": "crear_colaborador", "descripcion": "Puede crear colaboradores"},
    {"nombre": "editar_colaborador", "descripcion": "Puede editar colaboradores"},
    {"nombre": "eliminar_colaborador", "descripcion": "Puede eliminar colaboradores"},

    # Libro Diario
    {"nombre": "ver_libro_diario", "descripcion": "Puede ver libro diario"},
    # Libro Mayor
    {"nombre": "ver_libro_mayor", "descripcion": "Puede ver libro mayor"},
    # Balance General
    {"nombre": "ver_balance_general", "descripcion": "Puede ver el balance general"},
    # Estado Resultado
    {"nombre": "ver_estado_resultado", "descripcion": "Puede ver el estado resultado"},
    
]
    for data in permisos_data:
        # Crear permiso si no existe
        Permiso.objects.get_or_create(
            nombre=data["nombre"],
            defaults={"descripcion": data.get("descripcion", "")}
        )
