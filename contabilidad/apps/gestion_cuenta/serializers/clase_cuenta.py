from rest_framework import serializers
from ..models.clase_cuenta import ClaseCuenta
from ...empresa.models.empresa import Empresa

class ClaseCuentaCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClaseCuenta
        fields = [ "codigo" , "nombre"]

    def create(self, validated_data):
        request = self.context.get("request")
        empresa_id = request.auth['empresa']
        empresa = Empresa.objects.get(id=empresa_id) 
        validated_data["empresa"] = empresa
        return super().create(validated_data)
    
class ClaseCuentaDetailSerializer(serializers.ModelSerializer):
    padre = serializers.SerializerMethodField()
    class Meta:
        model = ClaseCuenta
        fields = ["id","codigo","nombre","padre"]
    
    def get_padre(self, obj):
        if obj.padre:
            return ClaseCuentaDetailSerializer(obj.padre).data
        return None
        
class ClaseCuentaListSerializer(serializers.ModelSerializer):
    padre = serializers.SerializerMethodField()
    class Meta:
        model = ClaseCuenta
        fields = ["id" , "codigo" , "nombre","padre"]
    def get_padre(self, obj):
        
        if obj.padre:
            return ClaseCuentaDetailSerializer(obj.padre).data 
        return None