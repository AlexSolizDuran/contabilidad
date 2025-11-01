from rest_framework import viewsets
from ..models import UserEmpresa
from ..serializers import (UserEmpresaCreateSerializer,
                           UserEmpresaDetailSerializer,
                           UserEmpresaListSerializer)


class UserEmpresaViewSet(viewsets.ModelViewSet):
    queryset = UserEmpresa.objects.all()
    serializer_class = UserEmpresaListSerializer
    def get_object(self):
        obj = super().get_object()
        print("ID solicitado:", self.kwargs["pk"])
        print("Queryset actual:", self.get_queryset())
        return obj
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
        # Por defecto, tomar la empresa del token (si existe)
        empresa_id = None
        try:
            if request.auth and hasattr(request.auth, 'get'):
                empresa_id = request.auth.get('empresa')
        except Exception:
            empresa_id = None

        # Construir queryset base: empresas aceptadas para la empresa del token
        from django.db.models import Q

        base_q = Q()
        if empresa_id:
            base_q |= Q(empresa=empresa_id, estado='ACEPTADA')

        # Además permitir que el propio usuario vea su relación (incluso si está PENDIENTE)
        if request.user and request.user.is_authenticated:
            base_q |= Q(usuario=request.user)

        queryset = UserEmpresa.objects.filter(base_q).distinct()

        if self.action == "list":
            # Solo usuarios normales, excluir roles admin
            queryset = queryset.exclude(roles__nombre='admin')

        return queryset

