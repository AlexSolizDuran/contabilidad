from ..models import PlantillaClase

def run():
    
    clase_cuenta_data = [
        {"codigo": 1, "nombre": "ACTIVO"},
        {"codigo": 11, "nombre": "ACTIVO CORRIENTE"},
        {"codigo": 111, "nombre": "EFECTIVO Y EQUIVALENTES DE EFECTIVO"},
        {"codigo": 112, "nombre": "INVERSIONES TEMPORALES"},
        {"codigo": 113, "nombre": "CUENTAS POR COBRAR COMERCIALES"},
        {"codigo": 114, "nombre": "CUENTAS POR COBRAR DIVERSAS"},
        {"codigo": 115, "nombre": "INVENTARIOS"},
        {"codigo": 116, "nombre": "GASTOS PAGADOS POR ANTICIPADO"},
        {"codigo": 12, "nombre": "ACTIVO NO CORRIENTE"},
        {"codigo": 121, "nombre": "INVERSIONES A LARGO PLAZO"},
        {"codigo": 122, "nombre": "PROPIEDADES, PLANTA Y EQUIPO"},
        {"codigo": 123, "nombre": "ACTIVOS INTANGIBLES"},
        {"codigo": 124, "nombre": "ACTIVOS DIFERIDOS"},
        {"codigo": 2, "nombre": "PASIVO"},
        {"codigo": 21, "nombre": "PASIVO CORRIENTE"},
        {"codigo": 211, "nombre": "OBLIGACIONES FINANCIERAS A CORTO PLAZO"},
        {"codigo": 212, "nombre": "CUENTAS POR PAGAR COMERCIALES"},
        {"codigo": 213, "nombre": "REMUNERACIONES POR PAGAR"},
        {"codigo": 214, "nombre": "IMPUESTOS POR PAGAR"},
        {"codigo": 22, "nombre": "PASIVO NO CORRIENTE"},
        {"codigo": 221, "nombre": "OBLIGACIONES FINANCIERAS A LARGO PLAZO"},
        {"codigo": 222, "nombre": "PROVISIONES A LARGO PLAZO"},
        {"codigo": 223, "nombre": "PASIVOS DIFERIDOS"},
        {"codigo": 3, "nombre": "PATRIMONIO"},
        {"codigo": 31, "nombre": "CAPITAL SOCIAL"},
        {"codigo": 32, "nombre": "RESERVAS"},
        {"codigo": 33, "nombre": "RESULTADOS ACUMULADOS"},
        {"codigo": 34, "nombre": "RESULTADO DEL EJERCICIO"},
    ]
    
    for data in custom_data:
        Custom.objects.get_or_create(nombre=data["nombre"],
            defaults={"color_primario": data["color_primario"],
                      "color_secundario": data["color_secundario"],
                      "color_terciario": data["color_terciario"]})

