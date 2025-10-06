from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from ..models.asiento_contable import AsientoContable
from ...empresa.models import UserEmpresa
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
        empresa = self.request.auth.get('empresa')  # o request.user.empresa.id según tu login
        if empresa:
                # Filtra los asientos que tengan al menos un movimiento cuya cuenta sea de la empresa
            return AsientoContable.objects.filter(
                movimientos__cuenta__empresa=empresa
            ).distinct()
        return AsientoContable.objects.none()

