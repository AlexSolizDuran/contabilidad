from ..models import PlantillaRol

def run():
    rol_data = [
        {"nombre": "admin"},
        {"nombre": "contador"},
        {"nombre": "auxiliar contable"},
        {"nombre":"auditor"}
    ]

    for data in rol_data:
        PlantillaRol.objects.get_or_create(nombre=data["nombre"])

