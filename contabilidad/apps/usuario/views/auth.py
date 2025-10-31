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
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'detail': 'Usuario registrado exitosamente'}, status=status.HTTP_201_CREATED)
