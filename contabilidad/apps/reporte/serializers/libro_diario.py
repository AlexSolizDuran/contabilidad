from rest_framework import serializers
from ...gestion_asiento.models import Movimiento

class LibroDiarioSerializer(serializers.ModelSerializer):
    cuenta = serializers.SerializerMethodField()
    asiento = serializers.SerializerMethodField()
    class Meta:
        model = Movimiento
        fields = ['id','referencia','debe','haber','cuenta','asiento']

    def get_asiento(self, obj):
        return {
            'id': obj.asiento_contable.id,
            'numero': obj.asiento_contable.numero,
            'fecha': obj.asiento_contable.created_at.date().isoformat(),
        }
    
    def get_cuenta(self, obj):
        return {
            'id' : obj.cuenta.id,
            'codigo' : obj.cuenta.codigo,
            'nombre' : obj.cuenta.nombre,
        }
        
