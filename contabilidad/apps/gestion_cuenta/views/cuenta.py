from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from ..models.cuenta import Cuenta
from ...gestion_asiento.models import Movimiento
from ...gestion_asiento.serializers import MovimientoListSerializer
from ..serializers.cuenta import (CuentaCreateSerializer,
                                  CuentaDetailSeriliazer,
                                  CuentaListSerializer)


class CuentaViewSet(viewsets.ModelViewSet):
    
    queryset = Cuenta.objects.all()
    serializer_class = CuentaListSerializer
    permission_classes = [IsAuthenticated]
    def get_serializer_class(self):
        if self.action == 'list':
            return CuentaListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return CuentaCreateSerializer
        elif self.action in ['retrieve','destroy']:
            return CuentaDetailSeriliazer
        return super().get_serializer_class()
    def get_queryset(self):
        request = self.request
        empresa = request.auth.get('empresa')  # o request.user.empresa.id según tu login
        return Cuenta.objects.filter(empresa_id=empresa)
    
    @action(detail=True, methods=['get'])
    def movimientos(self, request, pk=None):
        """
        GET /cuentas/{id}/movimientos/
        Devuelve los movimientos asociados a la cuenta
        """
        try:
            cuenta = self.get_object()  # Obtiene la cuenta según pk
        except Cuenta.DoesNotExist:
            return Response({"detail": "Cuenta no encontrada"}, status=404)

        movimientos = Movimiento.objects.filter(id_cuenta=cuenta.id)
        serializer = MovimientoListSerializer(movimientos, many=True)
        
        return Response(serializer.data)
