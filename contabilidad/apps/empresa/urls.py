from rest_framework import routers
from django.urls import path, include
from .views import (EmpresaViewSet,
                    CustomViewSet,
                    PermisoViewSet,
                    RolEmpresaViewSet,
                    UserEmpresaViewSet,
                    AuthViewSet,
                    FavoritoAPIView)
from .views.invitacion import AcceptInvitationView

router = routers.DefaultRouter()
router.register(r'empresa', EmpresaViewSet, basename='empresa')
router.register(r'custom', CustomViewSet, basename='custom')
router.register(r'permiso', PermisoViewSet, basename='permiso')
router.register(r'rol', RolEmpresaViewSet, basename='rol')
router.register(r'user_empresa', UserEmpresaViewSet, basename='user_empresa')
router.register(r'auth_empresa', AuthViewSet, basename='auth_empresa')


urlpatterns = [
    path('favorito/', FavoritoAPIView.as_view(), name='favorito'),
    path('favorito/<int:pk>/', FavoritoAPIView.as_view(), name='favorito-detalle'),

    path('', include(router.urls)),
    path('invitacion/accept/', AcceptInvitationView.as_view(), name='empresa-invitacion-accept'),
]
