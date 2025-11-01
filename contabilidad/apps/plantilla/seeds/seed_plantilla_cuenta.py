from ..models import PlantillaCuenta


def run():
    """Create a small set of sample plantilla cuentas.

    These accounts are created using `get_or_create` so running the seeder
    multiple times is idempotent.
    """

    plantilla_cuentas = [
    # 🟢 ACTIVO
    {"codigo": 11101, "nombre": "Caja y Bancos"},
    {"codigo": 11102, "nombre": "Caja General"},
    {"codigo": 11103, "nombre": "Cuentas Corrientes Bancarias"},
    {"codigo": 11201, "nombre": "Inversiones Temporales"},
    {"codigo": 11301, "nombre": "Clientes Nacionales"},
    {"codigo": 11302, "nombre": "Clientes del Exterior"},
    {"codigo": 11401, "nombre": "Anticipos a Proveedores"},
    {"codigo": 11501, "nombre": "Gastos Pagados por Anticipado"},
    {"codigo": 11601, "nombre": "Crédito Fiscal IVA"},
    {"codigo": 11602, "nombre": "Retenciones por Cobrar"},
    {"codigo": 12101, "nombre": "Cuentas por Cobrar a Largo Plazo"},
    {"codigo": 12201, "nombre": "Propiedades de Inversión"},
    {"codigo": 12301, "nombre": "Edificios y Construcciones"},
    {"codigo": 12302, "nombre": "Muebles y Equipos de Oficina"},
    {"codigo": 12303, "nombre": "Equipos de Cómputo"},
    {"codigo": 12401, "nombre": "Depreciación Acumulada de Bienes de Uso"},
    {"codigo": 12601, "nombre": "Inversiones Permanentes"},
    {"codigo": 12901, "nombre": "Activos Diferidos a Largo Plazo"},

    # 🔵 PASIVO
    {"codigo": 21101, "nombre": "Préstamos Bancarios a Corto Plazo"},
    {"codigo": 21201, "nombre": "Proveedores"},
    {"codigo": 21301, "nombre": "Cargas Sociales por Pagar"},
    {"codigo": 21401, "nombre": "IVA Débito Fiscal"},
    {"codigo": 21501, "nombre": "Provisiones a Corto Plazo"},
    {"codigo": 21601, "nombre": "Ingresos Diferidos Corto Plazo"},
    {"codigo": 22101, "nombre": "Préstamos Bancarios a Largo Plazo"},
    {"codigo": 22201, "nombre": "Proveedores a Largo Plazo"},
    {"codigo": 22301, "nombre": "Provisiones a Largo Plazo"},
    {"codigo": 22401, "nombre": "Pasivos Diferidos a Largo Plazo"},

    # 🟣 PATRIMONIO
    {"codigo": 31101, "nombre": "Capital Social"},
    {"codigo": 31201, "nombre": "Reserva Legal"},
    {"codigo": 31301, "nombre": "Resultados Acumulados"},
    {"codigo": 31401, "nombre": "Resultado del Ejercicio"},

    # 🟡 INGRESOS
    {"codigo": 41101, "nombre": "Ventas Netas"},
    {"codigo": 41102, "nombre": "Descuentos sobre Ventas"},
    {"codigo": 42101, "nombre": "Ingresos Financieros"},
    {"codigo": 43101, "nombre": "Otros Ingresos Operativos"},
    {"codigo": 43201, "nombre": "Ingresos Extraordinarios"},
    {"codigo": 44101, "nombre": "Ajustes y Diferencias de Cambio"},

    # 🔴 EGRESOS
    {"codigo": 51101, "nombre": "Costo de Ventas"},
    {"codigo": 51201, "nombre": "Costo de Producción"},
    {"codigo": 52101, "nombre": "Sueldos y Salarios"},
    {"codigo": 52201, "nombre": "Gastos de Oficina"},
    {"codigo": 52301, "nombre": "Servicios Profesionales"},
    {"codigo": 52401, "nombre": "Depreciaciones y Amortizaciones"},
    {"codigo": 52501, "nombre": "Impuestos y Tasas"},
    {"codigo": 53101, "nombre": "Publicidad y Marketing"},
    {"codigo": 53201, "nombre": "Gastos de Ventas"},
    {"codigo": 54101, "nombre": "Gastos Financieros"},
    {"codigo": 55101, "nombre": "Otros Gastos"},

    # ⚪ CUENTAS DE ORDEN
    {"codigo": 61101, "nombre": "Garantías Otorgadas"},
    {"codigo": 61201, "nombre": "Documentos en Custodia"},
    {"codigo": 61301, "nombre": "Valores en Tránsito"},
]

    for data in plantilla_cuentas:
        PlantillaCuenta.objects.get_or_create(
            codigo=data["codigo"],
            defaults={
                "nombre": data["nombre"],
                "estado": "ACTIVO",
            },
        )

