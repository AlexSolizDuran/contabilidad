from django.urls import path
from . import views

app_name = 'ia_reporte'

urlpatterns = [
    path('generar-reporte/', views.generar_reporte_ia, name='generar_reporte_ia'),
    path('ejemplos/', views.obtener_ejemplos_solicitudes, name='ejemplos_solicitudes'),
    path('info-empresa/', views.obtener_informacion_empresa, name='info_empresa'),
]
