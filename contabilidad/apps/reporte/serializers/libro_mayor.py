from rest_framework import serializers
from ...gestion_cuenta.models import Cuenta
from ...gestion_asiento.models import Movimiento

class MovimientoLibroMayorSerializer(serializers.ModelSerializer):
    fecha = serializers.SerializerMethodField()
    asiento = serializers.SerializerMethodField()
    class Meta:
        model = Movimiento
        fields = ['id','fecha','referencia','debe','haber','asiento']

    def get_fecha(self, obj):
        return obj.asiento_contable.created_at.date().isoformat()
    
    def get_asiento(self, obj):
        return obj.asiento_contable.numero


class LibroMayorSerializer(serializers.ModelSerializer):
    movimientos = MovimientoLibroMayorSerializer(many=True)

    class Meta:
        model = Cuenta
        fields = ['id','codigo','nombre','estado','movimientos']