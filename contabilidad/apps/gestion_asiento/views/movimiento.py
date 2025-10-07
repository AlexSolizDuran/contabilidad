from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from ..models.movimiento import Movimiento
from rest_framework import filters
from ...gestion_cuenta.models.cuenta import Cuenta
from ..serializers import (MovimientoCreateSerializer,
                           MovimientoDetailSerializer,
                           MovimientoListSerializer)


class MovimientoViewSet(viewsets.ModelViewSet):
    queryset = Movimiento.objects.all()
    serializer_class = MovimientoListSerializer
    permission_classes = [IsAuthenticated]
    
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['asiento_contable__numero', 'asiento_contable__created_at']
    ordering = ['asiento_contable__numero']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return MovimientoListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return MovimientoCreateSerializer
        elif self.action in ['retrieve','destroy']:
            return MovimientoDetailSerializer
        return super().get_serializer_class()
    
    def get_queryset(self):
        empresa = self.request.auth.get('empresa')  # o request.user.empresa.id según tu login
        if empresa:
            empresa_cuentas = Cuenta.objects.filter(empresa=empresa)
                # Filtra los movimientos cuya cuenta pertenece a la empresa
            return Movimiento.objects.filter(cuenta__in=empresa_cuentas)
        return Movimiento.objects.none()
