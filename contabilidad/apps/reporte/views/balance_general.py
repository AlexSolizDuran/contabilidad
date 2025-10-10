# apps/libro/views.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Sum
from ...gestion_cuenta.models import ClaseCuenta
from ...gestion_asiento.models import Movimiento
from datetime import datetime, timedelta

class BalanceGeneralViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    pagination_class = None  # desactiva paginación

    def list(self, request):
        # Parámetros de fecha
        fecha_inicio = request.query_params.get("fecha_inicio", "2010-01-01")
        fecha_fin = request.query_params.get("fecha_fin", datetime.now().strftime("%Y-%m-%d"))

        try:
            fecha_inicio_dt = datetime.strptime(fecha_inicio, "%Y-%m-%d")
            fecha_fin_dt = datetime.strptime(fecha_fin, "%Y-%m-%d") + timedelta(days=1)  # incluye todo el día
        except ValueError:
            return Response({"error": "Formato de fecha inválido. Use YYYY-MM-DD"}, status=400)

        # Empresa del usuario (ajustar según tu modelo)
        request = self.request
        empresa = request.auth.get('empresa')
        if not empresa:
            return Response({"error": "Usuario sin empresa asignada"}, status=400)

        # Traer todas las clases de la empresa y prefetch cuentas e hijos
        clases = (
            ClaseCuenta.objects.filter(empresa=empresa, padre=None, codigo__in=[1, 2, 3])
            .prefetch_related("hijos", "cuentas")
)

        # Función recursiva para calcular saldos
        def calcular_saldo(clase):
            # IDs de cuentas propias
            ids_cuenta = [cuenta.id for cuenta in clase.cuentas.all()]

            # Recursivamente sumar hijos
            hijos_data = []
            for hijo in clase.hijos.all():
                hijo_data = calcular_saldo(hijo)
                hijos_data.append(hijo_data)
                ids_cuenta.extend(hijo_data["ids"])

            # Movimientos de esas cuentas
            movimientos = Movimiento.objects.filter(
                cuenta_id__in=ids_cuenta,
                asiento_contable__created_at__gte=fecha_inicio_dt,
                asiento_contable__created_at__lt=fecha_fin_dt
            ).aggregate(
                total_debe=Sum("debe"),
                total_haber=Sum("haber")
            )

            total_debe = movimientos["total_debe"] or 0
            total_haber = movimientos["total_haber"] or 0
            saldo = total_debe - total_haber

            return {
                "codigo": clase.codigo,
                "nombre": clase.nombre,
                "total_debe": total_debe,
                "total_haber": total_haber,
                "saldo": saldo,
                "hijos": hijos_data,
                "ids": ids_cuenta,  # opcional, puedes eliminar si no necesitas
            }

        resultado = [calcular_saldo(clase) for clase in clases.filter(padre=None)]

        return Response(resultado)
