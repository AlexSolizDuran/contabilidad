from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from ...gestion_cuenta.models.cuenta import Cuenta
from ..serializers import LibroDiarioSerializer
from ...gestion_asiento.models import Movimiento

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

        # Solo movimientos cuyas cuentas pertenecen a la empresa
        qs = Movimiento.objects.filter(cuenta__empresa_id=empresa)

        # Mejora de rendimiento
        qs = qs.select_related('cuenta', 'asiento_contable')

        return qs
