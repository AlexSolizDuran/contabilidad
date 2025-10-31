from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AsientoContableViewSet,MovimientoViewSet

router = DefaultRouter()
router.register(r'asiento_contable', AsientoContableViewSet, basename='asiento_contable')
router.register(r'movimiento',MovimientoViewSet, basename='movimiento')

urlpatterns = [
    path('', include(router.urls)),   # incluye todas las rutas del ViewSet
]
