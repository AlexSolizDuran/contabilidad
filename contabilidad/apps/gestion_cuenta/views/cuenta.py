from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.db.models.functions import Cast, Substr
from django.db.models import CharField


from ..models import Cuenta,ClaseCuenta
from ...gestion_asiento.models import Movimiento
from ...gestion_asiento.serializers import MovimientoListSerializer
from ..serializers.cuenta import (CuentaCreateSerializer,
                                  CuentaDetailSeriliazer,
                                  CuentaListSerializer)


class CuentaViewSet(viewsets.ModelViewSet):
    
    queryset = Cuenta.objects.all()
    serializer_class = CuentaListSerializer
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return CuentaListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return CuentaCreateSerializer
        elif self.action in ['retrieve','destroy']:
            return CuentaDetailSeriliazer
        return super().get_serializer_class()
    
    def get_queryset(self):
        request = self.request
        empresa_id = request.auth.get('empresa')  # o request.user.empresa.id según tu login

        # Filtrar por empresa
        qs = Cuenta.objects.filter(empresa_id=empresa_id)

        # Filtrar por clase seleccionada si se pasa por query params
        clase_id = request.query_params.get('clase_id')
        if clase_id:
            try:
                clase = ClaseCuenta.objects.get(id=clase_id, empresa_id=empresa_id)
                # Obtener IDs de todos los descendientes
                descendientes_ids = clase.get_descendientes_ids()
                qs = qs.filter(clase_cuenta_id__in=descendientes_ids)
            except ClaseCuenta.DoesNotExist:
                qs = qs.none()

        # Convertimos codigo a char, luego extraemos el primer dígito y ordenamos
        qs = qs.annotate(
            codigo_str=Cast('codigo', CharField()),      # convierte a texto
            primer_digito=Substr('codigo_str', 1, 1)    # extrae primer dígito
        ).order_by('primer_digito', 'codigo')           # ordena por primer dígito y luego por código completo

        return qs
    
    @action(detail=True, methods=['get'])
    def movimientos(self, request, pk=None):
        """
        GET /cuentas/{id}/movimientos/
        Devuelve los movimientos asociados a la cuenta
        """
        try:
            cuenta = self.get_object()  # Obtiene la cuenta según pk
        except Cuenta.DoesNotExist:
            return Response({"detail": "Cuenta no encontrada"}, status=404)

        movimientos = Movimiento.objects.filter(id_cuenta=cuenta.id)
        serializer = MovimientoListSerializer(movimientos, many=True)
        
        return Response(serializer.data)
