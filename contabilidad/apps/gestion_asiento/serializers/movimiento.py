from rest_framework import serializers
from ..models.movimiento import Movimiento
from ...gestion_cuenta.serializers import CuentaListSerializer
from ...gestion_cuenta.models.cuenta import Cuenta
from ...gestion_asiento.models.asiento_contable import AsientoContable

class MovimientoCreateSerializer(serializers.ModelSerializer):
    cuenta = serializers.PrimaryKeyRelatedField(queryset=Cuenta.objects.all(), write_only=True)
    asiento_contable = serializers.PrimaryKeyRelatedField(queryset=AsientoContable.objects.all(), write_only=True)  
    class Meta:
        model = Movimiento
        fields = ["referencia", "cuenta", "debe","haber", "asiento_contable"]
        
    
        
class MovimientoDetailSerializer(serializers.ModelSerializer):
    cuenta = CuentaListSerializer()
    class Meta:
        model = Movimiento
        field = ["id","referencia","cuenta","debe","haber"]

        
        
class MovimientoListSerializer(serializers.ModelSerializer):
    cuenta = CuentaListSerializer()
    class Meta:
        model = Movimiento
        field = ["id","referencia","cuenta","debe","haber","asiento_contable"]

          
    def get_asiento_contable(self,obj):
        return {
            "id" : obj.asiento_contable.id,
            "numero" : obj.asiento_contable.numero,
            "fecha" : obj.asiento_contable.created_at.isoformat()
        }