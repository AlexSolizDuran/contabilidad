from rest_framework import generics, permissions
from ..serializers import RegisterSerializer,LoginSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny

class LoginView(generics.GenericAPIView):
    
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializer
    
    def post(self, request):
        
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        if user is not None:
            # Generar tokens sin empresa
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            # Respuesta con access token
            response = Response({
                'access': access_token
            }, status=status.HTTP_200_OK)

            # Guardar refresh token en cookie httpOnly
            response.set_cookie(
                key='refreshToken',
                value=refresh_token,
                httponly=True,       # JS no puede leerla
                secure=True,        # poner True en producción con HTTPS
                samesite='Strict',   # protección CSRF
                max_age=7*24*60*60   # duración en segundos (opcional)
            )

            return response
        return Response({'detail': 'Credenciales inválidas'}, status=status.HTTP_401_UNAUTHORIZED)
    
class LogoutView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        # Para logout, eliminamos la cookie del refresh token
        response = Response({"detail": "Logout exitoso"}, status=status.HTTP_200_OK)
        response.delete_cookie('refreshToken')  # borra la cookie httpOnly
        return response    
    
class RefreshTokenView(APIView):
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
# --- Registro de usuarios ---

class RegisterView(generics.CreateAPIView):
    
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]  # Cualquiera puede registrarse

