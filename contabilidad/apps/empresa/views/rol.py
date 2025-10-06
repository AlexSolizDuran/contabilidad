from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from ..models import RolEmpresa
from ..serializers import RolEmpresaCreateSerializer,RolEmpresaDetailSerializer,RolEmpresaListSerializer

class RolEmpresaViewSet(viewsets.ModelViewSet):
    queryset = RolEmpresa.objects.all()
    serializer_class = RolEmpresaListSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return RolEmpresaListSerializer
        elif self.action in ['create','update','partial_update']:
            return RolEmpresaCreateSerializer
        elif self.action in ['retrieve','destroy']:
            return RolEmpresaDetailSerializer
        return super().get_serializer_class()   
    
    def get_queryset(self):
        request = self.request
        empresa = request.auth.get('empresa')  # o request.user.empresa.id según tu login
        return RolEmpresa.objects.filter(empresa_id=empresa)
    
    @action(detail=True, methods=['post'])
    def set_usuarios(self, request, pk=None):
        """
        Actualiza la lista de usuarios de este rol.
        """
        rol = self.get_object()  # obtiene el rol por pk
        user_ids = request.data.get('usuarios', [])
        rol.usuarios.set(user_ids)  # actualiza la relación muchos a muchos
        return Response({"detail": "Usuarios actualizados correctamente"}, status=status.HTTP_200_OK)
    
    