from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from ...gestion_cuenta.models.cuenta import Cuenta
from ..serializers import LibroDiarioSerializer
from ...gestion_asiento.models import Movimiento
from django.utils.dateparse import parse_date
from rest_framework.response import Response
from django.db.models import Sum

class LibroDiarioViewSet(viewsets.ModelViewSet):
    serializer_class = LibroDiarioSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['asiento_contable__numero', 'asiento_contable__created_at']
    ordering = ['asiento_contable__numero']
    
    def get_queryset(self):
        request = self.request
        empresa = request.auth.get('empresa')  # o request.user.empresa.id según tu auth

        if not empresa:
            return Movimiento.objects.none()

        qs = Movimiento.objects.filter(cuenta__empresa_id=empresa)
        qs = qs.select_related('cuenta', 'asiento_contable')

        # Filtrar por fechas si se pasan en query params
        fecha_inicio = request.query_params.get('fecha_inicio')
        fecha_fin = request.query_params.get('fecha_fin')

        if fecha_inicio:
            fecha_inicio = parse_date(fecha_inicio)
            if fecha_inicio:
                qs = qs.filter(asiento_contable__created_at__date__gte=fecha_inicio)
        if fecha_fin:
            fecha_fin = parse_date(fecha_fin)
            if fecha_fin:
                qs = qs.filter(asiento_contable__created_at__date__lte=fecha_fin)

        return qs

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        # --- Calcular totales antes de la paginación ---
        totales = queryset.aggregate(
            debe_total=Sum('debe'),
            haber_total=Sum('haber')
        )

        # --- Aplicar paginación ---
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            response = self.get_paginated_response(serializer.data)
            response.data['totales'] = totales  # ✅ añadimos totales correctamente
            return response

        # --- Si no hay paginación ---
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'results': serializer.data,
            'totales': totales
        })
