from ..models import PlantillaCuenta

def run():
    
    custom_data = [
        
    ]
    
    for data in custom_data:
        Custom.objects.get_or_create(nombre=data["nombre"],
            defaults={"color_primario": data["color_primario"],
                      "color_secundario": data["color_secundario"],
                      "color_terciario": data["color_terciario"]})

