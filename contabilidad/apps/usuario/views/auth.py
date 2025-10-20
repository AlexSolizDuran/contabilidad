from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, generics
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema
from ..serializers import LoginSerializer, RegisterSerializer, UsuarioDetailSerializer
from django.contrib.auth import get_user_model
from ...utils.log import registrar_evento

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

            # 📝 Datos para el log
            datos_usuario = {
                "empresa": "empresa_001",  # ⚠️ reemplaza por la empresa real si la tienes
                "nombreEmpresa": "Mi Empresa de Prueba",
                "usuario": username,
                "nombre": f"{nombre} {apellido}",
                "rol": "Administrador" if user.is_staff else "Usuario",
                "ip": request.META.get("REMOTE_ADDR", "desconocida"),
                "dispositivo": "PC Escritorio",
                "sistema": request.headers.get("sec-ch-ua-platform", "desconocido"),
                "navegador": request.headers.get("User-Agent", "desconocido"),
                "idioma": request.headers.get("Accept-Language", "es-BO")
            }

            # 🪵 Registrar log al iniciar sesión
            registrar_evento(
                id_sesion=str(user.id),
                datos_usuario=datos_usuario,
                nivel="INFO",
                accion="Inicio de sesión",
                detalle=f"El usuario {username} inició sesión correctamente."
            )

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
