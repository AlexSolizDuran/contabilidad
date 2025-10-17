from django.urls import path, include
from rest_framework.routers import DefaultRouter

from rest_framework_simplejwt.views import TokenRefreshView
from .views import (UsuarioViewSet, LoginView, LogoutView, RefreshView, RegisterView)
#from .views import UsuarioViewSet

router = DefaultRouter()
router.register(r'usuario', UsuarioViewSet, basename='usuario')



urlpatterns = [
    path('auth/login/', LoginView.as_view(), name='auth-login'),
    path('auth/logout/', LogoutView.as_view(), name='auth-logout'),
    path('auth/refresh/', RefreshView.as_view(), name='auth-refresh'),
    path('auth/register/', RegisterView.as_view(), name='auth-register'),
    path('', include(router.urls)),
]
