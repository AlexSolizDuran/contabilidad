from rest_framework import serializers
from ..models.movimiento import Movimiento
from ...gestion_cuenta.serializers import CuentaListSerializer
from ...gestion_cuenta.models.cuenta import Cuenta
from ...gestion_asiento.models.asiento_contable import AsientoContable

class MovimientoCreateSerializer(serializers.ModelSerializer):
    cuenta = serializers.PrimaryKeyRelatedField(queryset=Cuenta.objects.all(), write_only=True)
    asiento_contable = serializers.PrimaryKeyRelatedField(queryset=AsientoContable.objects.all(), write_only=True ,required=False)  
    class Meta:
        model = Movimiento
        fields = ["referencia", "cuenta", "debe","haber", "asiento_contable"]
        
    
        
class MovimientoDetailSerializer(serializers.ModelSerializer):
    cuenta = CuentaListSerializer()
    class Meta:
        model = Movimiento
        fields = ["id","referencia","cuenta","debe","haber"]

        
        
class MovimientoListSerializer(serializers.ModelSerializer):
    cuenta = CuentaListSerializer()
    asiento = serializers.SerializerMethodField()  # <-- solo para lista

    class Meta:
        model = Movimiento
        fields = ["id", "referencia", "cuenta", "debe", "haber", "asiento"]

    def get_asiento(self, obj):
        # Devuelve solo los campos que quieras del asiento contable
        if obj.asiento_contable:
            return {
                "id": obj.asiento_contable.id,
                "numero": obj.asiento_contable.numero,
                "fecha": obj.asiento_contable.created_at.isoformat(),
                "estado": obj.asiento_contable.estado,
            }
        return None