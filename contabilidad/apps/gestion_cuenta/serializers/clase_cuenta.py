from rest_framework import serializers
from ..models.clase_cuenta import ClaseCuenta
from ...configurar.models.empresa import UserEmpresa

class ClaseCuentaCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClaseCuenta
        fields = [ "codigo" , "nombre"]

    def create(self, validated_data):
        print("entro al serializer")
        request = self.context.get("request")
        if not request or not request.user.is_authenticated:
            raise serializers.ValidationError("Usuario no autenticado")
        
        user_empresa = UserEmpresa.objects.filter(user=request.user).first()
        if not user_empresa:
            raise serializers.ValidationError("El usuario no tiene empresa asociada")

        validated_data["empresa"] = user_empresa.empresa
        return super().create(validated_data)
    
class ClaseCuentaDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClaseCuenta
        fields = ["id","codigo","nombre","padre","empresa","created_at"]
        
class ClaseCuentaListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClaseCuenta
        fields = ["id" , "codigo" , "nombre"]