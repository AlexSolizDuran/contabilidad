from rest_framework import serializers
from ..models import UserEmpresa

class LoginEmpresaSerializer(serializers.Serializer):
    empresa_id = serializers.UUIDField()  # Solo se envía el ID de la empresa

    def validate(self, data):
        empresa_id = data.get('empresa_id')
        user = self.context['request'].user  # Tomamos el usuario autenticado

        try:
            user_empresa = UserEmpresa.objects.get(usuario=user, empresa_id=empresa_id)
        except UserEmpresa.DoesNotExist:
            raise serializers.ValidationError("El usuario no pertenece a esta empresa")

        # Guardamos el objeto completo en validated_data para usarlo en la vista
        
        data['user_empresa'] = user_empresa
        return data
