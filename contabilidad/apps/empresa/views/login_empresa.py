from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from ..serializers import LoginEmpresaSerializer
from ...empresa.serializers import CustomDetailSerializer
from ...usuario.serializers import UsuarioDetailSerializer
from ..serializers import   UserEmpresaDetailSerializer
from ...empresa.models import Permiso
from ...utils.log import registrar_evento

class AuthViewSet(viewsets.ViewSet):
      # usuario ya logeado
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'])
    def login_empresa(self, request):
        print(request.data)
        serializer = LoginEmpresaSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        user_empresa = serializer.validated_data['user_empresa']
        ue = user_empresa
        user_obj = user_empresa.usuario
        empresa = user_empresa.empresa  
        custom = CustomDetailSerializer(user_empresa.custom).data
        user = UsuarioDetailSerializer(user_obj).data
        roles = user_empresa.roles.values_list('nombre', flat=True)
        permisos_list = list(
            Permiso.objects.filter(roles__in=user_empresa.roles.all())
            .values_list('nombre', flat=True)
            .distinct()
)
        refresh = RefreshToken.for_user(user_obj)   
        refresh['empresa'] = str(empresa.id)  # ✅ Guardamos la empresa en el token
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)
        datos_usuario = {
                "empresa": str(empresa.id),  # ⚠️ reemplaza por la empresa real si la tienes
                "nombreEmpresa": empresa.nombre,
                "usuario": user_obj.username,
                "nombre": user["persona"].get("nombre", "") + " " + user["persona"].get("apellido", ""),
                "rol": "Administrador" if user_obj.is_staff else "Usuario",
                "ip": request.META.get("REMOTE_ADDR", "desconocida"),
                "dispositivo": "PC Escritorio",
                "sistema": request.META.get("HTTP_SEC_CH_UA_PLATFORM") \
                                or request.META.get("OS") \
                                or "desconocido",
                "navegador": request.META.get("HTTP_USER_AGENT", "desconocido"),
                "idioma": request.META.get("HTTP_ACCEPT_LANGUAGE", "desconocido")
            }
        
            # 🪵 Registrar log al iniciar sesión
        registrar_evento(
            id_sesion=str(access_token),
            empresa_id=str(empresa.id),
            usuario_id=user_obj.id,
            datos_usuario=datos_usuario,
            nivel="INFO",
            accion="Inicio de sesión",
            detalle=f"El usuario {user_obj.username} inició sesión correctamente."
        )
        # --- Respuesta con cookies y access token ---
        response = Response({'access': access_token,
                             'empresa': empresa.id,
                             'user_empresa': user_empresa.id,
                             'usuario': user,
                             'roles': list(roles),
                             'permisos' : permisos_list,
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
