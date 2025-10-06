from rest_framework import serializers
from django.db.models import Max
from django.db import transaction
from ..models import AsientoContable,Movimiento
from ...empresa.models import Empresa
from .movimiento import MovimientoCreateSerializer,MovimientoDetailSerializer

class AsientoContableCreateSerializer(serializers.ModelSerializer):
    movimientos = MovimientoCreateSerializer(many=True)

    class Meta:
        model = AsientoContable
        fields = ["numero", "descripcion", "estado", "movimientos"]
        read_only_fields = ["numero"]  # numero se genera automáticamente

    def create(self, validated_data):
        movimientos_data = validated_data.pop('movimientos', [])

        # Obtener la empresa desde el request
        request = self.context.get("request")
        empresa_id = request.auth['empresa']  # asumiendo que el token trae id de empresa
        empresa = Empresa.objects.get(id=empresa_id)
        validated_data["empresa"] = empresa

        # Generar numero automáticamente por empresa
        with transaction.atomic():
            ultimo_numero = AsientoContable.objects.filter(empresa=empresa).aggregate(
                Max('numero')
            )['numero__max'] or 0
            validated_data['numero'] = ultimo_numero + 1

            asiento = AsientoContable.objects.create(**validated_data)

            for mov_data in movimientos_data:
                Movimiento.objects.create(asiento=asiento, **mov_data)

        return asiento

    def update(self, instance, validated_data):
        movimientos_data = validated_data.pop('movimientos', [])
        instance.descripcion = validated_data.get('descripcion', instance.descripcion)
        instance.estado = validated_data.get('estado', instance.estado)
        instance.save()

        # Eliminamos los movimientos antiguos y creamos los nuevos
        instance.movimientos.all().delete()
        for mov_data in movimientos_data:
            Movimiento.objects.create(asiento=instance, **mov_data)

        return instance

class AsientoContableDetailSerializer(serializers.ModelSerializer):
    movimientos = MovimientoDetailSerializer(many=True, read_only=True)

    class Meta:
        model = AsientoContable
        fields = ["id","descripcion", "numero","estado", "movimientos","created_at"]

class AsientoContableListSerializer(serializers.ModelSerializer):
    class Meta:
        model = AsientoContable
        fields = ["id","numero","descripcion","estado"]