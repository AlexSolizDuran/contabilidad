from ..models import PlantillaClase

def run():
    
    clase_cuenta_data = [
        # Nivel 1
        {"codigo": 1, "nombre": "ACTIVO"},
        {"codigo": 2, "nombre": "PASIVO"},
        {"codigo": 3, "nombre": "PATRIMONIO"},
        {"codigo": 4, "nombre": "INGRESOS"},
        {"codigo": 5, "nombre": "COSTOS Y GASTOS"},
        {"codigo": 6, "nombre": "CUENTAS DE ORDEN"},

        # Nivel 2
        {"codigo": 11, "nombre": "ACTIVO CORRIENTE"},
        {"codigo": 12, "nombre": "ACTIVO NO CORRIENTE"},
        {"codigo": 21, "nombre": "PASIVO CORRIENTE"},
        {"codigo": 22, "nombre": "PASIVO NO CORRIENTE"},
        {"codigo": 31, "nombre": "CAPITAL SOCIAL"},
        {"codigo": 32, "nombre": "RESERVAS"},
        {"codigo": 33, "nombre": "RESULTADOS ACUMULADOS"},
        {"codigo": 34, "nombre": "RESULTADO DEL EJERCICIO"},
        {"codigo": 41, "nombre": "VENTAS"},
        {"codigo": 42, "nombre": "OTROS INGRESOS"},
        {"codigo": 43, "nombre": "INGRESOS FINANCIEROS"},
        {"codigo": 51, "nombre": "COSTO DE VENTAS"},
        {"codigo": 52, "nombre": "GASTOS DE ADMINISTRACIÓN"},
        {"codigo": 53, "nombre": "GASTOS DE VENTA"},
        {"codigo": 54, "nombre": "GASTOS FINANCIEROS"},
        {"codigo": 55, "nombre": "OTROS GASTOS"},
        {"codigo": 61, "nombre": "CUENTAS DE ORDEN DEUDORAS"},
        {"codigo": 62, "nombre": "CUENTAS DE ORDEN ACREEDORAS"},

        # Nivel 3
        {"codigo": 111, "nombre": "EFECTIVO Y EQUIVALENTES"},
        {"codigo": 112, "nombre": "CUENTAS POR COBRAR"},
        {"codigo": 113, "nombre": "INVENTARIOS"},
        {"codigo": 114, "nombre": "OTROS ACTIVOS CORRIENTES"},
        {"codigo": 121, "nombre": "PROPIEDADES, PLANTA Y EQUIPO"},
        {"codigo": 122, "nombre": "ACTIVOS INTANGIBLES"},
        {"codigo": 123, "nombre": "INVERSIONES A LARGO PLAZO"},
        {"codigo": 124, "nombre": "OTROS ACTIVOS NO CORRIENTES"},
        {"codigo": 211, "nombre": "CUENTAS POR PAGAR"},
        {"codigo": 212, "nombre": "OBLIGACIONES FINANCIERAS"},
        {"codigo": 213, "nombre": "PROVISIONES CORRIENTES"},
        {"codigo": 214, "nombre": "OTROS PASIVOS CORRIENTES"},
        {"codigo": 221, "nombre": "PRÉSTAMOS A LARGO PLAZO"},
        {"codigo": 222, "nombre": "PROVISIONES A LARGO PLAZO"},
        {"codigo": 223, "nombre": "OTROS PASIVOS NO CORRIENTES"},
        {"codigo": 411, "nombre": "VENTAS DE MERCADERÍAS"},
        {"codigo": 412, "nombre": "VENTAS DE SERVICIOS"},
        {"codigo": 421, "nombre": "INGRESOS POR ALQUILERES"},
        {"codigo": 422, "nombre": "INGRESOS VARIOS"},
        {"codigo": 431, "nombre": "INTERESES GANADOS"},
        {"codigo": 432, "nombre": "OTROS INGRESOS FINANCIEROS"},
        {"codigo": 511, "nombre": "COSTO DE MERCADERÍAS VENDIDAS"},
        {"codigo": 512, "nombre": "COSTO DE SERVICIOS PRESTADOS"},
        {"codigo": 521, "nombre": "SUELDOS Y SALARIOS"},
        {"codigo": 522, "nombre": "SERVICIOS"},
        {"codigo": 523, "nombre": "OTROS GASTOS ADMINISTRATIVOS"},
        {"codigo": 531, "nombre": "COMISIONES"},
        {"codigo": 532, "nombre": "PUBLICIDAD Y PROMOCIÓN"},
        {"codigo": 541, "nombre": "INTERESES PAGADOS"},
        {"codigo": 542, "nombre": "COMISIONES BANCARIAS"},
        {"codigo": 551, "nombre": "GASTOS EXTRAORDINARIOS"},
        {"codigo": 552, "nombre": "PÉRDIDAS POR DIFERENCIAS CAMBIARIAS"}
    ]

    for data in clase_cuenta_data:
        PlantillaClase.objects.get_or_create(codigo=data["codigo"],
            defaults={"nombre": data["nombre"],
                      })

