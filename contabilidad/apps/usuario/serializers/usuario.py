from rest_framework import serializers
from ..models import (Persona,User)

class PersonaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Persona
        fields = ['nombre','apellido','telefono']

class PersonaDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Persona
        fields = ['nombre','apellido','telefono','ci']


class UsuarioListSerializer(serializers.ModelSerializer):
    persona = PersonaSerializer()
    class Meta:
        model = User
        fields = ['username','email','persona']
    
    

class UsuarioDetailSerializer(serializers.ModelSerializer):
    persona = PersonaDetailSerializer()
    class Meta:
        model = User
        fields = ['username','email','persona']

