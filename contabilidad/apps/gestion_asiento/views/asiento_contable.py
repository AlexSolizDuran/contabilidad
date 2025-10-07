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
        request = self.request
        empresa = request.auth.get('empresa')  # o request.user.empresa.id según tu login
        return AsientoContable.objects.filter(empresa_id=empresa)

