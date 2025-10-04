from rest_framework import serializers
from ..models.movimiento import Movimiento
from ...gestion_cuenta.models.cuenta import Cuenta
from ...gestion_asiento.models.asiento_contable import AsientoContable

class MovimientoCreateSerializer(serializers.ModelSerializer):
    cuenta = serializers.PrimaryKeyRelatedField(queryset=Cuenta.objects.all(), write_only=True)
    asiento_contable = serializers.PrimaryKeyRelatedField(queryset=AsientoContable.objects.all(), write_only=True)  
    class Meta:
        model = Movimiento
        fields = ["referencia", "cuenta", "debe","haber", "asiento_contable"]
        
    
        
class MovimientoDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movimiento
        field = ["id","referencia","cuenta","debe","haber","cuenta"]
    
    def get_cuenta(self,obj):
        return{
            "id" :obj.cuenta.id,
            "cuenta" : obj.cuenta.codigo + " - " + obj.cuenta.nombre,
        }  
        
class MovimientoListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movimiento
        field = ["id","referencia","cuenta","debe","haber","fecha","asiento_contable"]
    def get_fecha(self, obj):
        # devuelve el created_at en formato ISO o personalizado
        return obj.asiento_contable.created_at.isoformat()  
    def get_cuenta(self,obj):
        return{
            "id" :obj.cuenta.id,
            "cuenta" : obj.cuenta.codigo + " - " + obj.cuenta.nombre,
        }      
        
    def get_asiento_contable(self,obj):
        return {
            "id" : obj.asiento_contable.id,
            "asiento_contable" : obj.asiento_contable.numero
        }