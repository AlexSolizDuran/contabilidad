from rest_framework import serializers

class BalanceCuentaSerializer(serializers.Serializer):
    codigo = serializers.IntegerField()
    nombre = serializers.CharField()
    total_debe = serializers.DecimalField(max_digits=20, decimal_places=2)
    total_haber = serializers.DecimalField(max_digits=20, decimal_places=2)
    saldo = serializers.DecimalField(max_digits=20, decimal_places=2)
    hijos = serializers.ListSerializer(child=serializers.DictField(), required=False)
