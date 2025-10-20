from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import SuscripcionViewSet

router = DefaultRouter()
router.register(r'suscripcion', SuscripcionViewSet, basename='suscripcion')

urlpatterns = [
    path('', include(router.urls)),
]