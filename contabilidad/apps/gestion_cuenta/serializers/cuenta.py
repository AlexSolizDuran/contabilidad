from rest_framework import serializers
from ..models.cuenta import Cuenta
from ...configurar.models.empresa import UserEmpresa
from .clase_cuenta import ClaseCuentaListSerializer

class CuentaCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cuenta
        fields = ["codigo","nombre" , "estado",]
        
    def create(self, validated_data):
        request = self.context.get("request")
        if not request or not request.user.is_authenticated:
            raise serializers.ValidationError("Usuario no autenticado")

        # Obtener la empresa del usuario
        user_empresa = UserEmpresa.objects.filter(user=request.user).first()
        if not user_empresa:
            raise serializers.ValidationError("El usuario no tiene empresa asociada")

        # Asignar automáticamente la empresa
        validated_data["id_empresa"] = user_empresa.empresa
        return super().create(validated_data)        
    
class CuentaDetailSeriliazer(serializers.ModelSerializer):
    clase_cuenta = ClaseCuentaListSerializer()
    
    class Meta:
        model = Cuenta
        fields = ["id","codigo","nombre" , "estado","clase_cuenta","created_at" ]
        
class CuentaListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cuenta
        fields = ["id","codigo","nombre" ]
        

    