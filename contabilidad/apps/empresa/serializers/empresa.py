from rest_framework import serializers
from ..models import Empresa,RolEmpresa,UserEmpresa

from .user_empresa import UserEmpresaListSerializer



class EmpresaCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empresa
        fields = [ 'nombre','nit']
        
    def create(self, validated_data):
        usuario = self.context['request'].user
        empresa = Empresa.objects.create(**validated_data)
        user_empresa = UserEmpresa.objects.create(usuario=usuario, empresa=empresa)
        rol = RolEmpresa.objects.create(nombre='admin', empresa=empresa)
        user_empresa.roles.add(rol)
        return empresa
    
class EmpresaListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empresa
        fields = ['id','nombre']

class EmpresaDetailSerializer(serializers.ModelSerializer):
    usuarios = UserEmpresaListSerializer(many=True, read_only=True)

    class Meta:
        model = Empresa
        fields = ['id','nombre','nit','usuarios']
