from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from ..models import Permiso
from ..serializers import PermisoDetailSerializer,PermisoSerializer

class PermisoViewSet(viewsets.ModelViewSet):
    queryset = Permiso.objects.all()
    serializer_class = PermisoSerializer
    def get_serializer_class(self):
        if self.action in ['retrieve','destroy']:
            return PermisoDetailSerializer
        return super().get_serializer_class()
    
    @action(detail=True, methods=['post'])
    def update_permissions(self, request, pk=None):
        """
        Actualiza la lista de permisos de este rol.
        """
        rol = self.get_object()  # obtiene el rol por pk
        permiso_ids = request.data.get('permisos', [])
        rol.rol_permiso.set(permiso_ids)  # actualiza la relación muchos a muchos
        return Response({"detail": "Permisos actualizados correctamente"}, status=status.HTTP_200_OK)