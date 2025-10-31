from rest_framework import serializers
from typing import Dict, Any
from datetime import datetime

class SolicitudReporteSerializer(serializers.Serializer):
    """
    Serializer para recibir solicitudes de reportes en lenguaje natural.
    """
    texto_solicitud = serializers.CharField(
        max_length=1000,
        help_text="Descripción del reporte deseado en lenguaje natural"
    )
    
    def validate_texto_solicitud(self, value):
        if not value or len(value.strip()) < 10:
            raise serializers.ValidationError(
                "La solicitud debe tener al menos 10 caracteres"
            )
        return value.strip()


class InterpretacionSerializer(serializers.Serializer):
    """
    Serializer para la interpretación de la IA.
    """
    tipo_reporte = serializers.CharField()
    fecha_inicio = serializers.DateField(allow_null=True)
    fecha_fin = serializers.DateField(allow_null=True)
    cuentas_especificas = serializers.ListField(
        child=serializers.CharField(),
        allow_empty=True
    )
    clases_cuentas = serializers.ListField(
        child=serializers.CharField(),
        allow_empty=True
    )
    filtros_adicionales = serializers.DictField()
    agrupacion = serializers.CharField()
    ordenamiento = serializers.CharField()
    descripcion_interpretada = serializers.CharField()


class CuentaDetalleSerializer(serializers.Serializer):
    """
    Serializer para detalles de cuentas en reportes.
    """
    codigo = serializers.CharField()
    nombre = serializers.CharField()
    saldo = serializers.DecimalField(max_digits=15, decimal_places=3)


class ClaseDetalleSerializer(serializers.Serializer):
    """
    Serializer para detalles de clases en reportes.
    """
    codigo = serializers.CharField()
    nombre = serializers.CharField()
    total = serializers.DecimalField(max_digits=15, decimal_places=3)
    cuentas = CuentaDetalleSerializer(many=True, required=False)


class BalanceGeneralSerializer(serializers.Serializer):
    """
    Serializer para reporte de Balance General.
    """
    tipo = serializers.CharField()
    fecha_corte = serializers.DateField()
    activos = ClaseDetalleSerializer(many=True)
    pasivos = ClaseDetalleSerializer(many=True)
    patrimonio = ClaseDetalleSerializer(many=True)


class EstadoResultadosSerializer(serializers.Serializer):
    """
    Serializer para reporte de Estado de Resultados.
    """
    tipo = serializers.CharField()
    periodo = serializers.DictField()
    ingresos = serializers.DictField()
    costos_gastos = serializers.DictField()
    utilidad_bruta = serializers.DecimalField(max_digits=15, decimal_places=3)
    utilidad_operacional = serializers.DecimalField(max_digits=15, decimal_places=3)
    utilidad_neta = serializers.DecimalField(max_digits=15, decimal_places=3)


class MovimientoDetalleSerializer(serializers.Serializer):
    """
    Serializer para detalles de movimientos.
    """
    fecha = serializers.DateField()
    asiento = serializers.IntegerField()
    descripcion = serializers.CharField()
    referencia = serializers.CharField()
    debe = serializers.DecimalField(max_digits=15, decimal_places=3)
    haber = serializers.DecimalField(max_digits=15, decimal_places=3)


class CuentaLibroMayorSerializer(serializers.Serializer):
    """
    Serializer para cuentas en libro mayor.
    """
    cuenta = serializers.DictField()
    saldo_inicial = serializers.DecimalField(max_digits=15, decimal_places=3)
    total_debe = serializers.DecimalField(max_digits=15, decimal_places=3)
    total_haber = serializers.DecimalField(max_digits=15, decimal_places=3)
    saldo_final = serializers.DecimalField(max_digits=15, decimal_places=3)
    movimientos = MovimientoDetalleSerializer(many=True)


class LibroMayorSerializer(serializers.Serializer):
    """
    Serializer para reporte de Libro Mayor.
    """
    tipo = serializers.CharField()
    periodo = serializers.DictField()
    cuentas = CuentaLibroMayorSerializer(many=True)


class MovimientoLibroDiarioSerializer(serializers.Serializer):
    """
    Serializer para movimientos en libro diario.
    """
    cuenta_codigo = serializers.CharField()
    cuenta_nombre = serializers.CharField()
    referencia = serializers.CharField()
    debe = serializers.DecimalField(max_digits=15, decimal_places=3)
    haber = serializers.DecimalField(max_digits=15, decimal_places=3)


class AsientoLibroDiarioSerializer(serializers.Serializer):
    """
    Serializer para asientos en libro diario.
    """
    numero = serializers.IntegerField()
    fecha = serializers.DateField()
    descripcion = serializers.CharField()
    movimientos = MovimientoLibroDiarioSerializer(many=True)


class LibroDiarioSerializer(serializers.Serializer):
    """
    Serializer para reporte de Libro Diario.
    """
    tipo = serializers.CharField()
    periodo = serializers.DictField()
    asientos = AsientoLibroDiarioSerializer(many=True)


class ReporteResponseSerializer(serializers.Serializer):
    """
    Serializer para la respuesta completa del reporte generado por IA.
    """
    success = serializers.BooleanField()
    solicitud_original = serializers.CharField()
    interpretacion = serializers.DictField(required=False)
    reporte = serializers.DictField(required=False)
    fecha_generacion = serializers.DateTimeField(required=False, allow_null=True)
    empresa = serializers.CharField()
    error = serializers.CharField(required=False, allow_null=True)

    def to_representation(self, instance):
        """
        Si no se proporciona 'fecha_generacion', se inserta automáticamente
        la fecha y hora actual en formato ISO.
        """
        data = super().to_representation(instance)
        if not data.get("fecha_generacion"):
            data["fecha_generacion"] = datetime.utcnow().isoformat() + "Z"
        return data
