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
        fields = ['id','username','email','persona']

    
    
    

class UsuarioDetailSerializer(serializers.ModelSerializer):
    persona = PersonaDetailSerializer()
    old_password = serializers.CharField(write_only=True, required=False)
    new_password = serializers.CharField(write_only=True, required=False)
    class Meta:
        model = User
        fields = ['id','username','email','persona','old_password', 'new_password']
        extra_kwargs = {
            'persona': {'required': False},
        }

    def update(self, instance, validated_data):
        # Campos de persona
        persona_data = validated_data.pop('persona', {})
        for attr, value in persona_data.items():
            setattr(instance.persona, attr, value)
        instance.persona.save()

        # Cambiar contraseña si se proporciona
        old_password = validated_data.get('old_password')
        new_password = validated_data.get('new_password')
        if old_password and new_password:
            if not instance.check_password(old_password):
                raise serializers.ValidationError({'old_password': 'Contraseña actual incorrecta'})
            instance.set_password(new_password)

        instance.save()
        return instance