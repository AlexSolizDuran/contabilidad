from ..models import PlantillaClase

def run():
    
    clase_cuenta_data = [
        {"codigo": 1, "nombre": "ACTIVO"},
        {"codigo": 11, "nombre": "ACTIVO CORRIENTE"},
        {"codigo": 111, "nombre": "EFECTIVO Y EQUIVALENTES"},
        {"codigo": 112, "nombre": "CUENTAS POR COBRAR"},
        {"codigo": 113, "nombre": "INVENTARIOS"},
        {"codigo": 12, "nombre": "ACTIVO NO CORRIENTE"},
        {"codigo": 121, "nombre": "PROPIEDADES, PLANTA Y EQUIPO"},
        {"codigo": 122, "nombre": "ACTIVOS INTANGIBLES"},

        {"codigo": 2, "nombre": "PASIVO"},
        {"codigo": 21, "nombre": "PASIVO CORRIENTE"},
        {"codigo": 211, "nombre": "CUENTAS POR PAGAR"},
        {"codigo": 212, "nombre": "OBLIGACIONES FINANCIERAS"},
        {"codigo": 22, "nombre": "PASIVO NO CORRIENTE"},
        {"codigo": 221, "nombre": "PRÉSTAMOS A LARGO PLAZO"},

        {"codigo": 3, "nombre": "PATRIMONIO"},
        {"codigo": 31, "nombre": "CAPITAL SOCIAL"},
        {"codigo": 32, "nombre": "RESERVAS"},
        {"codigo": 33, "nombre": "RESULTADOS ACUMULADOS"},
        {"codigo": 34, "nombre": "RESULTADO DEL EJERCICIO"},

        {"codigo": 4, "nombre": "INGRESOS"},
        {"codigo": 41, "nombre": "VENTAS"},
        {"codigo": 42, "nombre": "OTROS INGRESOS"},

        {"codigo": 5, "nombre": "COSTOS Y GASTOS"},
        {"codigo": 51, "nombre": "COSTO DE VENTAS"},
        {"codigo": 52, "nombre": "GASTOS DE ADMINISTRACIÓN"},
        {"codigo": 53, "nombre": "GASTOS DE VENTA"},
        {"codigo": 54, "nombre": "GASTOS FINANCIEROS"},
        {"codigo": 55, "nombre": "OTROS GASTOS"},

        {"codigo": 6, "nombre": "CUENTAS DE ORDEN"}
    ]
    
    for data in clase_cuenta_data:
        PlantillaClase.objects.get_or_create(codigo=data["codigo"],
            defaults={"nombre": data["nombre"],
                      })

