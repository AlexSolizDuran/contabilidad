from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import (LibroMayorViewSet,
                    LibroDiarioViewSet)


router = DefaultRouter()
router.register(r'libro_mayor', LibroMayorViewSet, basename='libro_mayor')
router.register(r'libro_diario', LibroDiarioViewSet, basename='libro_diario')

urlpatterns = [
    path('', include(router.urls)),
]