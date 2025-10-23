from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import action
from ..models.clase_cuenta import ClaseCuenta

from ..serializers import (ClaseCuentaCreateSerializer,
                           ClaseCuentaDetailSerializer,
                           ClaseCuentaListSerializer,
                           ClaseCuentaDetailChildrenSerializer)
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
    
    @action(detail=False, methods=['get'])
    def arbol_cuenta(self, request):
        request = self.request
        empresa = request.auth.get('empresa')  # o request.user.empresa.id según tu login
        clase_cuenta = ClaseCuenta.objects.filter(empresa_id=empresa,codigo__gte=0, codigo__lte=9)
        clase_cuenta_serializer = ClaseCuentaDetailChildrenSerializer(clase_cuenta, many=True)
        return Response(clase_cuenta_serializer.data)
    

 