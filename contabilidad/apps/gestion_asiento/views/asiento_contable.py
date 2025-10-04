from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from ..models.asiento_contable import AsientoContable
from ...configurar.models.empresa import UserEmpresa
from ..serializers import (AsientoContableCreateSerializer,
                           AsientoContableListSerializer,
                           AsientoContableDetailSerializer)


class AsientoContableViewSet(viewsets.ModelViewSet):
    queryset = AsientoContable.objects.all()
    serializer_class = AsientoContableListSerializer
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return AsientoContableListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return AsientoContableCreateSerializer
        elif self.action in ['retrieve','destroy']:
            return AsientoContableDetailSerializer
        return super().get_serializer_class()
    
    def create(self, request, *args, **kwargs):
        print("Payload recibido:", request.data)  # 👈 aquí ves el JSON que envía el frontend
        return super().create(request, *args, **kwargs)
    
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            user_empresa = UserEmpresa.objects.filter(user=user).first()
            if user_empresa:
                # Filtra los asientos que tengan al menos un movimiento cuya cuenta sea de la empresa
                return AsientoContable.objects.filter(
                    movimientos__id_cuenta__id_empresa=user_empresa.empresa
                ).distinct()
        return AsientoContable.objects.none()

