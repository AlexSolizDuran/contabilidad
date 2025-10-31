from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from ..models.asiento_contable import AsientoContable
from ...empresa.models import UserEmpresa
from ..serializers import (AsientoContableCreateSerializer,
                           AsientoContableListSerializer,
                           AsientoContableDetailSerializer)
from ...utils.log import registrar_evento


class AsientoContableViewSet(viewsets.ModelViewSet):
    queryset = AsientoContable.objects.all()
    serializer_class = AsientoContableListSerializer
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return AsientoContableListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return AsientoContableCreateSerializer
        elif self.action in ['retrieve','destroy']:
            return AsientoContableDetailSerializer
        return super().get_serializer_class()
    
    def create(self, request, *args, **kwargs):
        # Ejecutar el create normal
        response = super().create(request, *args, **kwargs)

        # 🔹 Obtener token de sesión y empresa_id
        session_token = request.COOKIES.get("sessionToken") or request.headers.get('Authorization', '').split(' ')[-1]
        empresa_id = request.auth['empresa']
        usuario_id = request.user.id
        # Registrar evento
        registrar_evento(
            id_sesion=session_token,
            empresa_id=empresa_id,
            usuario_id=usuario_id,
            datos_usuario=None,  # No se repite info, la sesión ya existe
            nivel="INFO",
            accion="Creación de asiento contable",
            detalle=f"El usuario {usuario_id} creó un nuevo asiento contable con ID {response.data.get('numero')}"
        )

        return response

    def destroy(self, request, *args, **kwargs):
        # Obtener objeto antes de eliminarlo
        instance = self.get_object()
        asiento_id = getattr(instance, "id", "desconocido")

        # Ejecutar eliminación
        response = super().destroy(request, *args, **kwargs)

        # 🔹 Obtener token de sesión y empresa_id
        session_token = request.COOKIES.get("sessionToken")
        empresa_id = request.auth['empresa']
        usuario_id = request.user.id

        # Registrar evento
        registrar_evento(
            id_sesion=session_token,
            empresa_id=empresa_id,
            usuario_id=usuario_id,
            datos_usuario=None,
            nivel="WARNING",  # Nivel alto para operaciones sensibles
            accion="Eliminación de asiento contable",
            detalle=f"El usuario {usuario_id} eliminó el asiento contable con ID {asiento_id}."
        )

        return response
    
    def get_queryset(self):
        request = self.request
        empresa = request.auth.get('empresa')  # o request.user.empresa.id según tu login
        return AsientoContable.objects.filter(empresa_id=empresa)

