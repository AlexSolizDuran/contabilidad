from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from ..models import Empresa, UserEmpresa
from django.db.models import Q
from ..serializers import (EmpresaCreateSerializer,
                           EmpresaDetailSerializer,
                           EmpresaListSerializer)

class EmpresaViewSet(viewsets.ModelViewSet):
    queryset = Empresa.objects.all()
    serializer_class = EmpresaListSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'list':
            return EmpresaListSerializer
        elif self.action in ['create','update','partial_update']:
            return EmpresaCreateSerializer
        elif self.action in ['retrieve','destroy']:
            return EmpresaDetailSerializer
        return super().get_serializer_class()
    
    @action(detail=False, methods=['get'])
    def mis_empresas(self, request):
        user = request.user
        # Mostrar empresas donde el usuario tiene la relación aceptada
        # O mostrar empresas donde el usuario es administrador (las que creó)
        user_empresas = UserEmpresa.objects.filter(usuario=user).filter(Q(estado='ACEPTADA') | Q(roles__nombre='admin')).distinct()
        empresas = [ue.empresa for ue in user_empresas]
        serializer = EmpresaListSerializer(empresas, many=True)

        return Response(serializer.data)
