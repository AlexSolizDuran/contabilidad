from rest_framework import serializers
from ..models import AsientoContable,Movimiento
from .movimiento import MovimientoCreateSerializer,MovimientoDetailSerializer

class AsientoContableCreateSerializer(serializers.ModelSerializer):
    movimientos = MovimientoCreateSerializer(many=True, required=False, allow_empty=True)

    class Meta:
        model = AsientoContable
        fields = ["numero","descripcion", "estado", "movimientos"]

    def __init__(self, *args, **kwargs):
        # Se puede pasar 'include_movimientos' al serializer para controlar la salida
        include_movimientos = kwargs.pop('include_movimientos', False)
        super().__init__(*args, **kwargs)
        if not include_movimientos:
            self.fields.pop('movimientos')  # quitar el campo movimientos si no queremos mostrarlo

    def create(self, validated_data):
        movimientos_data = validated_data.pop("movimientos", [])  # por defecto lista vacía
        asiento = AsientoContable.objects.create(**validated_data)
        for mov_data in movimientos_data:
            Movimiento.objects.create(id_asiento_contable=asiento, **mov_data)
        return asiento

class AsientoContableDetailSerializer(serializers.ModelSerializer):
    movimientos = MovimientoDetailSerializer(many=True, read_only=True)

    class Meta:
        model = AsientoContable
        fields = ["id","descripcion", "numero","estado", "movimientos","created_at"]

class AsientoContableListSerializer(serializers.ModelSerializer):
    class Meta:
        model = AsientoContable
        fields = ["id","numero","descripcion","estado"]