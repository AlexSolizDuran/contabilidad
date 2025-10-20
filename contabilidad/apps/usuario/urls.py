from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UsuarioViewSet, LoginView  # solo LoginView

# Configuramos el router para el ViewSet de Usuario
router = DefaultRouter()
router.register(r'usuario', UsuarioViewSet, basename='usuario')

urlpatterns = [
    # Ruta para login
    path('auth/login/', LoginView.as_view(), name='auth-login'),

    # Incluimos las rutas del router
    path('', include(router.urls)),
]
