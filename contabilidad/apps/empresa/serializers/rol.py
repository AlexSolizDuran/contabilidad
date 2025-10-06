from rest_framework import serializers
from ..models import RolEmpresa,UserEmpresa,Empresa


class RolEmpresaCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = RolEmpresa
        fields = ['nombre']
        
    def create(self, validated_data):
        
        request = self.context.get("request")
        empresa_id = request.auth['empresa_id']
        empresa = Empresa.objects.get(id=empresa_id) 
        rol = RolEmpresa.objects.create(empresa=empresa, **validated_data)
        return rol

class RolEmpresaListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = RolEmpresa
        fields = ['id','nombre']

class RolEmpresaDetailSerializer(serializers.ModelSerializer):
    usuarios = serializers.PrimaryKeyRelatedField(many=True, queryset=UserEmpresa.objects.all())

    class Meta:
        model = RolEmpresa
        fields = ['id','nombre','empresa','usuarios']