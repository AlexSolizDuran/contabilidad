from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from ..models.movimiento import Movimiento
from ...configurar.models.empresa import UserEmpresa
from ...gestion_cuenta.models.cuenta import Cuenta
from ..serializers import (MovimientoCreateSerializer,
                           MovimientoDetailSerializer,
                           MovimientoListSerializer)


class MovimientoViewSet(viewsets.ModelViewSet):
    queryset = Movimiento.objects.all()
    serializer_class = MovimientoListSerializer
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return MovimientoListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return MovimientoCreateSerializer
        elif self.action in ['retrieve','destroy']:
            return MovimientoDetailSerializer
        return super().get_serializer_class()
    
    def get_queryset(self):
        print("entro al view")
        user = self.request.user
        if user.is_authenticated:
            user_empresa = UserEmpresa.objects.filter(user=user).first()
            if user_empresa:
                empresa_cuentas = Cuenta.objects.filter(id_empresa=user_empresa.empresa)
                # Filtra los movimientos cuya cuenta pertenece a la empresa
                return Movimiento.objects.filter(id_cuenta__in=empresa_cuentas)
        return Movimiento.objects.none()
