from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from ..serializers import LoginEmpresaSerializer
from ...empresa.serializers import CustomDetailSerializer
from ...usuario.serializers import UsuarioDetailSerializer




class AuthViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]  # usuario ya logeado

    @action(detail=False, methods=['post'])
    def login_empresa(self, request):
        serializer = LoginEmpresaSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        user_empresa = serializer.validated_data['user_empresa']
        user = user_empresa.usuario
        empresa = user_empresa.empresa  
        custom = CustomDetailSerializer(user_empresa.custom).data
        user = UsuarioDetailSerializer(user).data
        roles = user_empresa.roles.values_list('nombre', flat=True)
        refresh = RefreshToken.for_user(user)

        refresh['empresa'] = str(empresa.id)  # ✅ Guardamos la empresa en el token

        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        # --- Respuesta con cookies y access token ---
        response = Response({'access': access_token,
                             'empresa': empresa.id,
                             'user_empresa': user_empresa.id,
                             'usuario': user,
                             'roles': list(roles),
                             'custom': custom
                             }, 
                            status=status.HTTP_200_OK)
        response.set_cookie(
            key='sessionToken',
            value=access_token,
            httponly=True,
            secure=True,
            samesite='Strict',
            max_age=7*24*60*60
        )
        return response
