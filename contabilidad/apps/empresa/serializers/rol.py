from rest_framework import serializers
from ..models import RolEmpresa,Empresa,UserEmpresa,Permiso
from ...usuario.serializers import UsuarioDetailSerializer
from .permiso import PermisoSerializer


class RolEmpresaCreateSerializer(serializers.ModelSerializer):
    usuarios = serializers.PrimaryKeyRelatedField(many=True, queryset=UserEmpresa.objects.all(),required=False)
    permisos = serializers.PrimaryKeyRelatedField(
            many=True, queryset=Permiso.objects.all(), required=False    )
    class Meta:
        model = RolEmpresa
        fields = ['nombre','usuarios','permisos']
        
    def create(self, validated_data):
        
        request = self.context.get("request")
        empresa_id = request.auth['empresa']
        empresa = Empresa.objects.get(id=empresa_id) 
        rol = RolEmpresa.objects.create(empresa=empresa, **validated_data)
        return rol
    
    def update(self, instance, validated_data):
        # Actualiza nombre
        instance.nombre = validated_data.get('nombre', instance.nombre)
        instance.save()

        # Actualiza usuarios
        usuarios = validated_data.get('usuarios')
        if usuarios is not None:
            instance.usuarios.set(usuarios)

        # Actualiza permisos
        permisos = validated_data.get('permisos')
        if permisos is not None:
            instance.permisos.set(permisos)

        return instance

class RolEmpresaListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = RolEmpresa
        fields = ['id','nombre']

class UserDetailSerializer(serializers.ModelSerializer):
    usuario = UsuarioDetailSerializer()
    class Meta:
        model = UserEmpresa
        fields = ['id','usuario']
        
class RolEmpresaDetailSerializer(serializers.ModelSerializer):
    usuarios = UserDetailSerializer(many=True, read_only=True)
    permisos = PermisoSerializer(many=True, read_only=True)
    class Meta:
        model = RolEmpresa
        fields = ['id','nombre','empresa','usuarios','permisos']