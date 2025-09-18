from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from ..models import Empresa, UserEmpresa
from ..serializers import EmpresaSerializer

class EmpresaViewSet(viewsets.ModelViewSet):
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            # Filtra las empresas donde está el usuario y devuelve solo la primera
            return Empresa.objects.filter(userempresa__user=user)[:1]
        return Empresa.objects.none()  # Ninguna empresa si no está autenticado

    def perform_create(self, serializer):
        # Creamos la empresa y asociamos al usuario autenticado automáticamente
        empresa = serializer.save()
        #aqui se crea la tabla intermedia de user - empresa  el user que lo crea obtiene el rol admin de la empresa
        UserEmpresa.objects.create(user=self.request.user, empresa=empresa, rol='admin')
