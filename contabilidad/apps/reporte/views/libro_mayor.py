from rest_framework import viewsets
from django.db.models.functions import Cast, Substr
from rest_framework.permissions import IsAuthenticated
from django.db.models import CharField,Count
from ..serializers import LibroMayorSerializer
from ...gestion_cuenta.models import Cuenta,ClaseCuenta


class LibroMayorViewSet(viewsets.ModelViewSet):
    serializer_class = LibroMayorSerializer
    permission_classes = [IsAuthenticated]
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

    
        # Solo cuentas con movimientos
        qs = qs.annotate(num_mov=Count('movimientos')).filter(num_mov__gt=0)
        # Convertimos codigo a char, luego extraemos el primer dígito y ordenamos
        qs = qs.annotate(
            codigo_str=Cast('codigo', CharField()),      # convierte a texto
            primer_digito=Substr('codigo_str', 1, 1)    # extrae primer dígito
        ).order_by('primer_digito', 'codigo')           # ordena por primer dígito y luego por código completo

        return qs
