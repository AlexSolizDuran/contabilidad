from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import SuscripcionViewSet, PagoExitosoCallback

router = DefaultRouter()
router.register(r'suscripcion', SuscripcionViewSet, basename='suscripcion')

urlpatterns = [
    path('', include(router.urls)),
    path('suscripcion/pago_exitoso', PagoExitosoCallback.as_view(), name='pago_exitoso_callback'), # 🚨 NUEVA RUTA
]