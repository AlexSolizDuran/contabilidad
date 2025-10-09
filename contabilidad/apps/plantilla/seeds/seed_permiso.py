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
    {"nombre": "crear_movimiento", "descripcion": "Puede crear movimientos"},
    {"nombre": "editar_movimiento", "descripcion": "Puede editar movimientos"},
    {"nombre": "eliminar_movimiento", "descripcion": "Puede eliminar movimientos"},

    # Libro Diario
    {"nombre": "ver_libro_diario", "descripcion": "Puede ver libro diario"},

    # Libro Mayor
    {"nombre": "ver_libro_mayor", "descripcion": "Puede ver libro mayor"},
    
]


    for data in permisos_data:
        # Crear permiso si no existe
        permiso, creado = Permiso.objects.get_or_create(
            nombre=data["nombre"],
            defaults={"descripcion": data.get("descripcion", "")}
        )
