from rest_framework import serializers
from ..models import UserEmpresa,Custom
from ...usuario.models import User
from ...usuario.serializers import UsuarioDetailSerializer
from .rol import RolEmpresaListSerializer

class CustomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Custom
        fields = ['id','nombre', 'color_primario', 'color_secundario', 'color_terciario']
        
class UserEmpresaCreateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True,required=False)  # nuevo campo para recibir el correo
    texto_tipo = serializers.CharField(required=False)
    texto_tamaño = serializers.CharField(required=False)
    custom = serializers.PrimaryKeyRelatedField(queryset=Custom.objects.all(), required=False)

    
    class Meta:
        model = UserEmpresa
        fields = ['email', 'custom', 'texto_tipo', 'texto_tamaño']  # usuario se obtiene del gmail, empresa se asigna automáticamente

    def validate_email(self, value):
        """Validar que el usuario exista"""
        try:
            usuario = User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("Usuario no existe")
        return usuario  # retornamos el objeto usuario en lugar del correo

    def create(self, validated_data):
        request = self.context.get("request")
        empresa_id = request.auth['empresa']  # obtienes la empresa del token/auth
        user = validated_data.pop('email')  # es el objeto User retornado en validate_gmail
        
        usuario = User.objects.get(username=user)

        # Verificar si ya existe la relación
        from ..models import Empresa
        empresa = Empresa.objects.get(pk=empresa_id)
        if UserEmpresa.objects.filter(usuario=usuario, empresa=empresa).exists():
            raise serializers.ValidationError("El usuario ya es colaborador de esta empresa")

        # Crear instancia
        custom = Custom.objects.get(nombre='verde')
        user_empresa = UserEmpresa.objects.create(usuario=usuario, empresa=empresa,custom=custom, **validated_data)
        return user_empresa

class UserEmpresaListSerializer(serializers.ModelSerializer):
    usuario = UsuarioDetailSerializer()
    roles = RolEmpresaListSerializer(many=True, read_only=True)
    class Meta:
        model = UserEmpresa
        fields = ['id','usuario','roles']

class UserEmpresaDetailSerializer(serializers.ModelSerializer):
    roles = RolEmpresaListSerializer(many=True, read_only=True)
    custom = CustomSerializer(read_only=True)
    class Meta:
        model = UserEmpresa
        fields = ['id','usuario','empresa','roles','custom','texto_tipo','texto_tamaño']