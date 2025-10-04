from rest_framework import viewsets
from ..models.clase_cuenta import ClaseCuenta
from ...configurar.models.empresa import UserEmpresa
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
        print("entro al view")
        user = self.request.user
        if user.is_authenticated:
            # Obtener la primera relación UserEmpresa del usuario
            user_empresa = UserEmpresa.objects.filter(user=user).first()
            
            if user_empresa:
                # Filtrar cuentas solo de esa empresa
                return ClaseCuenta.objects.filter(id_empresa=user_empresa.empresa)
        # Ninguna cuenta si no hay usuario autenticado o sin empresa asociada
        return ClaseCuenta.objects.none()
    