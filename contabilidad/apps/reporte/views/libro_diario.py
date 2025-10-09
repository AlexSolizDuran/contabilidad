from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from ...gestion_cuenta.models.cuenta import Cuenta
from ..serializers import LibroDiarioSerializer
from ...gestion_asiento.models import Movimiento
from django.utils.dateparse import parse_date

class LibroDiarioViewSet(viewsets.ModelViewSet):
    serializer_class = LibroDiarioSerializer
    permission_classes = [IsAuthenticated]
    
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['asiento_contable__numero', 'asiento_contable__created_at']
    ordering = ['asiento_contable__numero']
    
    def get_queryset(self):
        request = self.request
        empresa = request.auth.get('empresa')  # o request.user.empresa.id según tu login

        if not empresa:
            return Movimiento.objects.none()

        qs = Movimiento.objects.filter(cuenta__empresa_id=empresa)
        qs = qs.select_related('cuenta', 'asiento_contable')

        # Filtrar por fecha si se pasa en query params
        fecha_inicio = request.query_params.get('fecha_inicio')
        fecha_fin = request.query_params.get('fecha_fin')

        if fecha_inicio:
            fecha_inicio = parse_date(fecha_inicio)
            if fecha_inicio:
                qs = qs.filter(asiento_contable__created_at__date__gte=fecha_inicio)
        if fecha_fin:
            fecha_fin = parse_date(fecha_fin)
            if fecha_fin:
                qs = qs.filter(asiento_contable__created_at__date__lte=fecha_fin)

        return qs
