from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CuentaViewSet,ClaseCuentaViewSet

router = DefaultRouter()
router.register(r'cuentas', CuentaViewSet, basename='cuenta')
router.register(r'clase_cuenta',ClaseCuentaViewSet, basename='clase_cuenta')

urlpatterns = [
    path('', include(router.urls)),   # incluye todas las rutas del ViewSet
]
