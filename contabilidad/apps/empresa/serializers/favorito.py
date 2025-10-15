from rest_framework import serializers
from ..models import Favorito, UserEmpresa

class FavoritoCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Favorito
        fields = [ 'ruta', 'nombre']
    
    
class FavoritoListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Favorito
        fields = ['id',  'ruta', 'nombre']