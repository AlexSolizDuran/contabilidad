from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core import signing
from django.conf import settings
from ..models import UserEmpresa
from ...usuario.models import User
from ..models import Empresa


class AcceptInvitationView(APIView):
    permission_classes = []  # permitir acceso público ya que el token valida

    def get(self, request):
        token = request.query_params.get('token')
        if not token:
            return Response({'detail': 'Token requerido'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            data = signing.loads(token, salt='empresa-invite', max_age=60 * 60 * 24 * 7)  # 7 días
            user_id = data.get('user_id')
            empresa_id = data.get('empresa_id')
        except signing.BadSignature:
            return Response({'detail': 'Token inválido'}, status=status.HTTP_400_BAD_REQUEST)
        except signing.SignatureExpired:
            return Response({'detail': 'Token expirado'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({'detail': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        try:
            empresa = Empresa.objects.get(pk=empresa_id)
        except Empresa.DoesNotExist:
            return Response({'detail': 'Empresa no encontrada'}, status=status.HTTP_404_NOT_FOUND)

        # Buscar o crear la relación user_empresa
        ue, created = UserEmpresa.objects.get_or_create(usuario=user, empresa=empresa)
        # Marcar como aceptada
        ue.texto_tipo = 'ACEPTADA'
        ue.estado = 'ACEPTADA'
        ue.save()

        return Response({'detail': 'Invitación aceptada'}, status=status.HTTP_200_OK)
