from rest_framework import serializers

from ..models import AsientoContable,Movimiento
from ...empresa.models import Empresa
from .movimiento import MovimientoCreateSerializer,MovimientoDetailSerializer

class AsientoContableCreateSerializer(serializers.ModelSerializer):
    movimientos = MovimientoCreateSerializer(many=True)

    class Meta:
        model = AsientoContable
        fields = ["numero", "descripcion", "estado", "movimientos"]
        read_only_fields = ["numero"]  # numero generado automáticamente en el modelo

    def create(self, validated_data):
        print("llego aqui" , validated_data)
        movimientos_data = validated_data.pop('movimientos', [])
        
        # Obtener la empresa desde el request
        request = self.context.get("request")
        empresa_id = request.auth['empresa']  # asumiendo que el token trae id de empresa
        empresa = Empresa.objects.get(id=empresa_id)
        validated_data["empresa"] = empresa

        # Crear el asiento; el número se generará automáticamente en el modelo
        asiento = AsientoContable.objects.create(**validated_data)

        # Crear los movimientos relacionados
        for mov_data in movimientos_data:
            Movimiento.objects.create(asiento_contable=asiento, **mov_data)

        return asiento

    def update(self, instance, validated_data):
        movimientos_data = validated_data.pop('movimientos', [])
        instance.descripcion = validated_data.get('descripcion', instance.descripcion)
        instance.estado = validated_data.get('estado', instance.estado)
        instance.save()

        # Reemplazar movimientos antiguos con los nuevos
        instance.movimientos.all().delete()
        for mov_data in movimientos_data:
            Movimiento.objects.create(asiento_contable=instance, **mov_data)

        return instance


class AsientoContableDetailSerializer(serializers.ModelSerializer):
    movimientos = MovimientoDetailSerializer(many=True, read_only=True)
    fecha = serializers.SerializerMethodField()
    class Meta:
        model = AsientoContable
        fields = ["id","descripcion", "numero","estado", "movimientos","fecha"]
        
    def get_fecha(self,obj):
        return obj.created_at.date().isoformat()


class AsientoContableListSerializer(serializers.ModelSerializer):
    fecha = serializers.SerializerMethodField()

    class Meta:
        model = AsientoContable
        fields = ["id", "numero", "descripcion", "estado", "fecha"]

    def get_fecha(self, obj):
        # Si tu modelo tiene un campo created_at tipo DateTimeField:
        return obj.created_at.date().isoformat()