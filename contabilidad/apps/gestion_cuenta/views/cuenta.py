from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from ...configurar.models.empresa import UserEmpresa
from ..models.cuenta import Cuenta
from ...gestion_asiento.models.movimiento import Movimiento
from ...gestion_asiento.serializers.movimiento import MovimientoSerializer
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
        user = self.request.user
        if user.is_authenticated:
            # Obtener la primera relación UserEmpresa del usuario
            user_empresa = UserEmpresa.objects.filter(user=user).first()
            if user_empresa:
                # Filtrar cuentas solo de esa empresa
                return Cuenta.objects.filter(id_empresa=user_empresa.empresa)
        # Ninguna cuenta si no hay usuario autenticado o sin empresa asociada
        return Cuenta.objects.none()
    
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
        serializer = MovimientoSerializer(movimientos, many=True)
        
        return Response(serializer.data)
