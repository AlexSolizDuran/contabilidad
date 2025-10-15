from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.permissions import AllowAny
from ..serializers import UsuarioListSerializer, UsuarioDetailSerializer
from ..models import User

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsuarioListSerializer
    def get_serializer_class(self):
        if self.action == 'list':
            return UsuarioListSerializer
        elif self.action in ['create','update','partial_update']:
            return UsuarioDetailSerializer
        elif self.action in ['retrieve','destroy']:
            return UsuarioDetailSerializer
        return super().get_serializer_class()



