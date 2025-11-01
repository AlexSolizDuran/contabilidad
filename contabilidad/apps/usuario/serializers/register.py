from rest_framework import serializers
from ..models import (Persona,User)
from .usuario import PersonaSerializer
from django.core.mail import send_mail
from django.core import signing
from django.conf import settings



class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    persona = PersonaSerializer()

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'persona']
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True}
        }

    def create(self, validated_data):
        persona_data = validated_data.pop('persona')
        persona = Persona.objects.create(**persona_data)
        
        user = User(
            persona=persona,
            username=validated_data['username'],
            email=validated_data.get('email', '')
        )
        user.set_password(validated_data['password'])  # encripta la contraseña
        # verified por defecto False
        user.verified = False
        user.save()

        # Generar token firmado para verificación (expira en 24h)
        token = signing.dumps({'user_id': user.id}, salt='email-verification')

        # Construir enlace de verificación usando el nombre de la ruta (asegura que la URL exista)
        from django.urls import reverse
        public = getattr(settings, 'DJANGO_PUBLIC_URL', '')
        path = reverse('auth-verify') + f"?token={token}"
        if public:
            # Si se definió DJANGO_PUBLIC_URL en .env, usarlo (evita IPs internas de contenedores)
            verify_url = f"{public}{path}"
        else:
            request = self.context.get('request') if hasattr(self, 'context') else None
            if request is not None:
                verify_url = request.build_absolute_uri(path)
            else:
                verify_url = path

        subject = 'Verifica tu cuenta'
        html_body = f"<p>Hola {persona.nombre},</p><p>Por favor confirma tu correo haciendo clic en el siguiente enlace:</p><p><a href='{verify_url}'>{verify_url}</a></p>"

        # Enviar correo usando configuración SMTP (Django send_mail)
        try:
            send_mail(subject, '', from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', None), recipient_list=[user.email], html_message=html_body)
        except Exception:
            # No interrumpir el registro si el correo falla; log depende del backend
            pass

        return user


