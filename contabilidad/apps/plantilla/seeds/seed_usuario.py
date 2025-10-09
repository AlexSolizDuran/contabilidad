from ...usuario.models import User,Persona

def run():
    
    custom_data = [
        {"nombre": "verde", "color_primario": "#439E3A", "color_secundario": "#7DD177", "color_terciario": "#CBFFC7"},
        {"nombre": "rojo", "color_primario": "#C0392B", "color_secundario": "#E57373", "color_terciario": "#F9C0C0"},
        {"nombre": "azul", "color_primario": "#2980B9", "color_secundario": "#5DADE2", "color_terciario": "#C7EBFF"},
        {"nombre": "morado", "color_primario": "#8E44AD", "color_secundario": "#B569C4", "color_terciario": "#E0BBF3"},
        {"nombre": "amarillo", "color_primario": "#F1C40F", "color_secundario": "#F7DC6F", "color_terciario": "#FFF9D6"},
        {"nombre": "naranja", "color_primario": "#E67E22", "color_secundario": "#F5B041", "color_terciario": "#FDEBD0"},
        {"nombre": "gris", "color_primario": "#7F8C8D", "color_secundario": "#BDC3C7", "color_terciario": "#ECF0F1"},
        {"nombre": "marron", "color_primario": "#8B4513", "color_secundario": "#A0522D", "color_terciario": "#D2B48C"},
        {"nombre": "turquesa", "color_primario": "#1ABC9C", "color_secundario": "#48C9B0", "color_terciario": "#A3E4D7"},
    ]
    
    for data in custom_data:
        Custom.objects.get_or_create(nombre=data["nombre"],
            defaults={"color_primario": data["color_primario"],
                      "color_secundario": data["color_secundario"],
                      "color_terciario": data["color_terciario"]})

