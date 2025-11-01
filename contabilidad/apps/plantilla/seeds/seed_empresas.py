from ...empresa.models.empresa import Empresa
from ...empresa.models.user_empresa import UserEmpresa
from contabilidad.apps.empresa.models.custom import Custom
from contabilidad.apps.empresa.models.rol import RolEmpresa
from ...usuario.models.usuario import Persona, User
from ...gestion_cuenta.models.cuenta import Cuenta
from ...gestion_asiento.models.asiento_contable import AsientoContable
from ...gestion_asiento.models.movimiento import Movimiento
from decimal import Decimal
from datetime import datetime, timedelta
import random
from django.utils import timezone


def run():
    """Create a sample Empresa, a User and link them via UserEmpresa.

    Idempotent: uses get_or_create so it is safe to run multiple times.
    """

    # Datos de ejemplo
    empresa_data = {
        "nombre": "Empresa Demo S.A.",
        "nit": 123456789,
    }

    persona_data = {
        "nombre": "Ayrton",
        "apellido": "Desarrollador",
        "ci": "0000000",
        "telefono": "+59170000000",
    }

    username = "admin2"
    password = "123456"
    email = "admin2@gmail.com"
    # Crear o obtener Persona
    persona, _ = Persona.objects.get_or_create(
        nombre=persona_data["nombre"],
        apellido=persona_data["apellido"],
        defaults={
            "ci": persona_data["ci"],
            "telefono": persona_data["telefono"],
        },
    )

    # Crear o obtener usuario
    user, created_user = User.objects.get_or_create(
        username=username,
        defaults={
            "email": email,
            "persona": persona,
            "verified": True,
            "is_staff": True,
        },
    )
    if created_user:
        user.set_password(password)
        user.save()

    # Crear o obtener empresa
    empresa, _ = Empresa.objects.get_or_create(
        nombre=empresa_data["nombre"], defaults={"nit": empresa_data["nit"]}
    )

    custom, _ = Custom.objects.get_or_create(nombre="verde")

    rol, _ = RolEmpresa.objects.get_or_create(nombre="admin", empresa=empresa)



    # Vincular usuario y empresa en UserEmpresa
    ue, _ = UserEmpresa.objects.get_or_create(usuario=user, empresa=empresa, custom=custom)

    # Enlazar el rol con la relación intermedia UserEmpresa (no con User directo)
    rol.usuarios.add(ue)

    print(f"Seed empresas: usuario={user.username} (created={created_user}), empresa={empresa.nombre}, vinculo_id={ue.id if hasattr(ue, 'id') else 'n/a'}")

    activos = Cuenta.objects.filter(empresa=empresa, codigo__startswith="1")
    pasivos = Cuenta.objects.filter(empresa=empresa, codigo__startswith="2")
    patrimonio = Cuenta.objects.filter(empresa=empresa, codigo__startswith="3")
    ingresos = Cuenta.objects.filter(empresa=empresa, codigo__startswith="4")
    egresos = Cuenta.objects.filter(empresa=empresa, codigo__startswith="5")

    if not activos or not ingresos:
        print("❌ ERROR: No hay cuentas contables creadas. Ejecuta primero el seeder de cuentas.")
        return

    asiento_creados = 0

    for i in range(500):
        descripcion = f"Asiento Demo Auto {i + 1}"

        dias_atras = random.randint(90, 1460)
        fecha = timezone.now().date() - timedelta(days=dias_atras)
        # Convertir fecha (date) a datetime consciente del timezone para evitar warnings
        try:
            fecha_datetime = datetime.combine(fecha, datetime.min.time())
            fecha_aware = timezone.make_aware(fecha_datetime)
        except Exception:
            # Fallback: usar timezone.now() si la conversión falla
            fecha_aware = timezone.now()

        asiento, created = AsientoContable.objects.get_or_create(
            empresa=empresa, descripcion=descripcion, defaults={"estado": "APROBADO"}
        )

        if not created:
            continue

        AsientoContable.objects.filter(pk=asiento.pk).update(created_at=fecha_aware)

        monto_base = random.choice([100, 200, 350, 500, 750, 1000, 2500, 5000])

        # ============================
        # NUEVA LÓGICA VARIADA
        # ============================

        # Selección aleatoria de cuentas y montos variables
        cuentas = [
            *list(activos), *list(pasivos), *list(patrimonio),
            *list(ingresos), *list(egresos)
        ]

        random.shuffle(cuentas)
        movimientos = []

        total_debe = Decimal("0")
        total_haber = Decimal("0")

        for cuenta in cuentas[:random.randint(2, 4)]:
            monto = Decimal(str(round(monto_base * random.uniform(0.5, 1.5), 2)))

            # Aplicar la lógica contable según tipo de cuenta
            codigo = str(cuenta.codigo)

            if codigo.startswith("1"):  # Activos
                debe = monto if random.choice([True, False]) else Decimal("0")
                haber = Decimal("0") if debe > 0 else monto

            elif codigo.startswith("5"):  # Egresos
                debe = monto
                haber = Decimal("0")

            elif codigo.startswith("4"):  # Ingresos
                debe = Decimal("0")
                haber = monto

            elif codigo.startswith("3"):  # Patrimonio
                debe = Decimal("0")
                haber = monto

            elif codigo.startswith("2"):  # Pasivos
                debe = monto if random.choice([True, False]) else Decimal("0")
                haber = Decimal("0") if debe > 0 else monto

            else:
                continue

            total_debe += debe
            total_haber += haber

            movimientos.append({
                "referencia": f"REF-{i+1}-{cuenta.codigo}",
                "debe": debe,
                "haber": haber,
                "cuenta": cuenta,
            })

        # Ajustar para que Debe == Haber
        diferencia = total_debe - total_haber
        if diferencia != 0:
            # Ajustar el último movimiento para cuadrar el asiento
            ultimo = movimientos[-1]
            if diferencia > 0:
                ultimo["haber"] += diferencia
            else:
                ultimo["debe"] += abs(diferencia)

        # Crear movimientos en BD
        for mov in movimientos:
            Movimiento.objects.create(
                referencia=mov["referencia"],
                debe=mov["debe"],
                haber=mov["haber"],
                cuenta=mov["cuenta"],
                asiento_contable=asiento,
            )

        asiento_creados += 1

    print(f"✅ Se crearon {asiento_creados} asientos contables con mayor variación en debe y haber.")
