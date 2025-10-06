from rest_framework import serializers
from ..models import UserEmpresa


class LoginEmpresaSerializer(serializers.Serializer):
    empresa_id = serializers.UUIDField()
    user_id = serializers.UUIDField()

    def validate(self, data):
        empresa_id = data.get('empresa_id')
        user_id = data.get('user_id')

        # Verificar que exista la relación usuario-empresa
        try:
            user_empresa = UserEmpresa.objects.get(usuario_id=user_id, empresa_id=empresa_id)
        except UserEmpresa.DoesNotExist:
            raise serializers.ValidationError("El usuario no pertenece a esta empresa")

        data['user_empresa'] = user_empresa
        return data