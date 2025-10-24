from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import (LibroMayorViewSet,
                    LibroDiarioViewSet,
                    BalanceGeneralViewSet,
                    DescargarLogEmpresaView)


router = DefaultRouter()
router.register(r'libro_mayor', LibroMayorViewSet, basename='libro_mayor')
router.register(r'libro_diario', LibroDiarioViewSet, basename='libro_diario')
router.register(r'balance_general', BalanceGeneralViewSet, basename='balance_general')  

urlpatterns = [
    path('logs/descargar/', DescargarLogEmpresaView.as_view(), name='descargar-log-empresa'),

    path('', include(router.urls)),
]