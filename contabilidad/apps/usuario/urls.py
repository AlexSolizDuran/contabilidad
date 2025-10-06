from django.urls import path, include
from rest_framework.routers import DefaultRouter

from rest_framework_simplejwt.views import TokenRefreshView
from .views import (UsuarioViewSet,AuthViewSet)
#from .views import UsuarioViewSet

router = DefaultRouter()
router.register(r'usuario', UsuarioViewSet, basename='usuario')
router.register(r'auth', AuthViewSet, basename='auth')



urlpatterns = [
    
    path('', include(router.urls)),
]
