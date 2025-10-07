from rest_framework import serializers
from ..models.cuenta import Cuenta
from ...empresa.models.empresa import Empresa
from .clase_cuenta import ClaseCuentaListSerializer

class CuentaCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cuenta
        fields = ["codigo","nombre" , "estado",]
        
    def create(self, validated_data):
        request = self.context.get("request")
        empresa_id = request.auth['empresa']
        empresa = Empresa.objects.get(id=empresa_id) 
        validated_data["empresa"] = empresa
        return super().create(validated_data)        
    
class CuentaDetailSeriliazer(serializers.ModelSerializer):
    clase_cuenta = ClaseCuentaListSerializer()
    
    class Meta:
        model = Cuenta
        fields = ["id","codigo","nombre" , "estado","clase_cuenta"]
        
class CuentaListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cuenta
        fields = ["id","codigo","nombre" ]
        

    