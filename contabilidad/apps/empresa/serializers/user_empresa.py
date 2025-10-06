from rest_framework import serializers
from ..models import UserEmpresa
from .rol import RolEmpresaListSerializer


class UserEmpresaCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserEmpresa
        fields = ['usuario', 'empresa']
    
    def create(self, validated_data):
        request = self.context.get("request")
        empresa_id = request.auth['empresa']
        validated_data["empresa"] = empresa_id
        return super().create(validated_data)

class UserEmpresaListSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserEmpresa
        fields = ['id','usuario','empresa']

class UserEmpresaDetailSerializer(serializers.ModelSerializer):
    roles = RolEmpresaListSerializer(many=True, read_only=True)

    class Meta:
        model = UserEmpresa
        fields = ['id','usuario','empresa','roles']