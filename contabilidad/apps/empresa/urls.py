from rest_framework import routers
from django.urls import path, include
from .views import (EmpresaViewSet,
                    CustomViewSet,
                    PermisoViewSet,
                    RolEmpresaViewSet,
                    UserEmpresaViewSet,
                    AuthViewSet)

router = routers.DefaultRouter()
router.register(r'empresa', EmpresaViewSet, basename='empresa')
router.register(r'custom', CustomViewSet, basename='custom')
router.register(r'permiso', PermisoViewSet, basename='permiso')
router.register(r'rol', RolEmpresaViewSet, basename='rol')
router.register(r'user_empresa', UserEmpresaViewSet, basename='user_empresa')
router.register(r'auth_empresa', AuthViewSet, basename='auth_empresa')


urlpatterns = [
    path('', include(router.urls)),
]
