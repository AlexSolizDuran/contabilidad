from rest_framework import serializers
from ..models import Custom

class CustomCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Custom
        fields = ['nombre', 'color_primario', 'color_secundario', 'color_terciario']
        
class CustomDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Custom
        fields =['id','nombre','color_primario','color_secundario','color_terciario']
    
class CustomListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Custom
        fields = ['id','nombre','color_primario','color_secundario','color_terciario']