from rest_framework import serializers
from ..models import Permiso,RolEmpresa

class PermisoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Permiso
        fields = ['id', 'nombre', 'descripcion']
        
class PermisoDetailSerializer(serializers.ModelSerializer):
    roles = serializers.PrimaryKeyRelatedField(many=True, queryset=RolEmpresa.objects.all(),write_only=True)

    class Meta:
        model = Permiso
        fields =['id','nombre','descripcion','roles']