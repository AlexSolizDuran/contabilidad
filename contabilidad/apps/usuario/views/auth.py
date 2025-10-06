from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from ..serializers import LoginSerializer, RegisterSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class AuthViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=['post'])
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        if user:
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            response = Response({'access': access_token}, status=status.HTTP_200_OK)
            response.set_cookie(
                key='refreshToken',
                value=refresh_token,
                httponly=True,
                secure=True,
                samesite='Strict',
                max_age=7*24*60*60
            )
            return response

        return Response({'detail': 'Credenciales inválidas'}, status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, methods=['post'])
    def logout(self, request):
        response = Response({'detail': 'Logout exitoso'}, status=status.HTTP_200_OK)
        response.delete_cookie('refreshToken')
        return response

    @action(detail=False, methods=['post'])
    def refresh(self, request):
        refresh_token = request.COOKIES.get('refreshToken')
        if not refresh_token:
            return Response({'detail': 'No refresh token'}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)
            return Response({'access': access_token})
        except:
            return Response({'detail': 'Token inválido o expirado'}, status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'detail': 'Usuario registrado exitosamente'}, status=status.HTTP_201_CREATED)
