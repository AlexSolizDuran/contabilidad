from rest_framework import viewsets
from ..models.clase_cuenta import ClaseCuenta

from ..serializers import (ClaseCuentaCreateSerializer,
                           ClaseCuentaDetailSerializer,
                           ClaseCuentaListSerializer)
from rest_framework.permissions import IsAuthenticated

class ClaseCuentaViewSet(viewsets.ModelViewSet):
    queryset = ClaseCuenta.objects.all()
    serializer_class = ClaseCuentaListSerializer
    permission_classes = [IsAuthenticated]
    def get_serializer_class(self):
        if self.action == 'list':
            return ClaseCuentaListSerializer
        elif self.action in ['create','update','partial_update']:
            return ClaseCuentaCreateSerializer
        elif self.action in ['retrieve','destroy']:
            return ClaseCuentaDetailSerializer
        return super().get_serializer_class()
    
    def get_queryset(self):
        request = self.request
        empresa = request.auth.get('empresa')  # o request.user.empresa.id según tu login
        return ClaseCuenta.objects.filter(empresa_id=empresa)
    