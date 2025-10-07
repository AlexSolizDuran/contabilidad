from rest_framework import serializers




class LibroMayorSerializer(serializers.Serializer):
    cuenta_id = serializers.UUIDField(required=True)
    fecha_inicio = serializers.DateField(required=True)
    fecha_fin = serializers.DateField(required=True)