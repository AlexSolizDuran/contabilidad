from rest_framework import serializers
from django.contrib.auth import authenticate, get_user_model
from django.core import signing
from django.core.mail import send_mail
from django.conf import settings


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if not (username and password):
            raise serializers.ValidationError("Debe ingresar username y password")

        User = get_user_model()

        # Intentar autenticar normalmente
        user = authenticate(username=username, password=password)
        if user and (not hasattr(user, 'verified') or getattr(user, 'verified')):
            data['user'] = user
            return data

        # Si no autenticó, intentar encontrar usuario por email o username
        candidate = None
        try:
            candidate = User.objects.filter(email__iexact=username).first()
            if not candidate:
                candidate = User.objects.filter(username__iexact=username).first()
        except Exception:
            candidate = None

        # Si existe usuario candidato
        if candidate:
            # Si no está verificado, reenviar correo y devolver mensaje solicitado
            if hasattr(candidate, 'verified') and not getattr(candidate, 'verified'):
                token = signing.dumps({'user_id': candidate.id}, salt='email-verification')
                from django.urls import reverse
                public = getattr(settings, 'DJANGO_PUBLIC_URL', '')
                path = reverse('auth-verify') + f"?token={token}"
                if public:
                    verify_url = f"{public}{path}"
                else:
                    try:
                        request = self.context.get('request') if hasattr(self, 'context') else None
                        if request is not None:
                            verify_url = request.build_absolute_uri(path)
                        else:
                            verify_url = path
                    except Exception:
                        verify_url = path

                subject = 'Reenvío de verificación'
                nombre = getattr(getattr(candidate, 'persona', None), 'nombre', '')
                html_body = f"<p>Hola {nombre},</p><p>Por favor confirma tu correo haciendo clic en el siguiente enlace:</p><p><a href='{verify_url}'>{verify_url}</a></p>"
                try:
                    send_mail(subject, '', from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', None), recipient_list=[candidate.email], html_message=html_body)
                except Exception:
                    pass

                raise serializers.ValidationError("Verifica el email, Correo de verificacion reenviado")

        # Si no existe candidato o no coincide la contraseña
        raise serializers.ValidationError("Credenciales invalidas")