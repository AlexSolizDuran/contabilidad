from rest_framework import viewsets
from ..models import UserEmpresa
from ..serializers import (UserEmpresaCreateSerializer,
                           UserEmpresaDetailSerializer,
                           UserEmpresaListSerializer)


class UserEmpresaViewSet(viewsets.ModelViewSet):
    queryset = UserEmpresa.objects.all()
    serializer_class = UserEmpresaListSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return UserEmpresaListSerializer
        elif self.action in ['create','update','partial_update']:
            return UserEmpresaCreateSerializer
        elif self.action in ['retrieve','destroy']:
            return UserEmpresaDetailSerializer
        return super().get_serializer_class()
    
    def get_queryset(self):
        request = self.request
        empresa = request.auth.get('empresa')

        return UserEmpresa.objects.filter(empresa=empresa) \
        .exclude(roles__nombre='admin') \
        .distinct()