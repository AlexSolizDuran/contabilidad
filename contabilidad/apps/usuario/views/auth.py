from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, generics
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema
from ..serializers import LoginSerializer, RegisterSerializer, UsuarioDetailSerializer
from django.contrib.auth import get_user_model


User = get_user_model()

class LoginView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        if user:
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
            nombre = user.persona.nombre
            apellido = user.persona.apellido
            email = user.email
            username = user.username

           

            response = Response(
                {
                    'access': access_token,
                    'user_id': user.id,
                    'username': username,
                    'nombre': nombre,
                    'superuser': user.is_staff,
                    'apellido': apellido,
                    'email': email
                },
                status=status.HTTP_200_OK
            )
            response.set_cookie(
                key='sessionToken',
                value=access_token,
                httponly=True,
                secure=True,
                samesite='Strict',
                max_age=60*60*24
            )
            return response

        return Response({'detail': 'Credenciales inválidas'}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        response = Response({'detail': 'Logout exitoso'}, status=status.HTTP_200_OK)
        response.delete_cookie('refreshToken')
        return response


class RefreshView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        refresh_token = request.COOKIES.get('refreshToken')
        if not refresh_token:
            return Response({'detail': 'No refresh token'}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)
            return Response({'access': access_token})
        except:
            return Response({'detail': 'Token inválido o expirado'}, status=status.HTTP_401_UNAUTHORIZED)


class RegisterView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = RegisterSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'detail': 'Usuario registrado exitosamente'}, status=status.HTTP_201_CREATED)


class VerifyEmailView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        token = request.query_params.get('token')
        if not token:
            return Response({'detail': 'Token requerido'}, status=status.HTTP_400_BAD_REQUEST)
        from django.core import signing
        try:
            data = signing.loads(token, salt='email-verification', max_age=60*60*24)
            user_id = data.get('user_id')
        except signing.BadSignature:
            return Response({'detail': 'Token inválido'}, status=status.HTTP_400_BAD_REQUEST)
        except signing.SignatureExpired:
            return Response({'detail': 'Token expirado'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(pk=user_id)
            user.verified = True
            user.save()
            return Response({'detail': 'Correo verificado, ya puedes iniciar sesión'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'detail': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)


class ResendVerificationView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        identifier = request.data.get('email') or request.data.get('username')
        if not identifier:
            return Response({'detail': 'email o username requerido'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            if '@' in identifier:
                user = User.objects.get(email=identifier)
            else:
                user = User.objects.get(username=identifier)
        except User.DoesNotExist:
            return Response({'detail': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        if user.verified:
            return Response({'detail': 'Usuario ya verificado'}, status=status.HTTP_400_BAD_REQUEST)

        # generar token y reenviar correo
        from django.core import signing
        from django.core.mail import send_mail
        from django.conf import settings

        token = signing.dumps({'user_id': user.id}, salt='email-verification')
        from django.urls import reverse
        public = getattr(settings, 'DJANGO_PUBLIC_URL', '')
        path = reverse('auth-verify') + f"?token={token}"
        if public:
            verify_url = f"{public}{path}"
        else:
            verify_url = request.build_absolute_uri(path)

        subject = 'Reenvío de verificación'
        html_body = f"<p>Hola {user.persona.nombre},</p><p>Por favor confirma tu correo haciendo clic en el siguiente enlace:</p><p><a href='{verify_url}'>{verify_url}</a></p>"
        try:
            send_mail(subject, '', from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', None), recipient_list=[user.email], html_message=html_body)
        except Exception:
            pass

        return Response({'detail': 'Correo de verificación reenviado si el usuario existe'}, status=status.HTTP_200_OK)
