from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from .models import Suscripcion, Estado, TipoPlan, Pago # Importamos TipoPlan
from .serializers import SuscripcionDetailSerializer, TipoPlanSerializer, PaymentRequestSerializer, SubscriptionSuccessSerializer
from datetime import timedelta
from django.db import transaction
from datetime import date
import uuid

class SuscripcionViewSet(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = SuscripcionDetailSerializer

    def get_queryset(self):
        # Devuelve las suscripciones del usuario autenticado
        return Suscripcion.objects.filter(user=self.request.user)

    @action(detail=False, methods=['get'], url_path='activa')
    def get_suscripcion_activa(self, request):
        """
        Endpoint: GET /suscripcion/activa/
        1. Devuelve la suscripción activa del usuario.
        2. Si no hay, devuelve una lista de planes disponibles (TipoPlan) con código 404.
        """
        
        # 1. Busca el estado 'activo'
        try:
            estado_activo = Estado.objects.get(nombre='activo')
        except Estado.DoesNotExist:
            return Response({"detail": "Estado 'activo' no configurado."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # 2. Busca la suscripción activa más reciente para el usuario
        suscripcion = self.get_queryset().filter(estado=estado_activo).order_by('-fecha_inicio').first()

        if suscripcion:
            # Si se encuentra, devuelve la suscripción
            serializer = self.get_serializer(suscripcion)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        # 3. SI NO HAY SUSCRIPCIÓN ACTIVA: Devolver los planes disponibles con 404
        
        # Obtenemos todos los TipoPlan y prefetchamos las relaciones anidadas
        planes_disponibles = TipoPlan.objects.all().select_related('plan', 'caracteristica')
        
        # Usamos TipoPlanSerializer (necesitas asegurarte de que está importado correctamente)
        serializer = TipoPlanSerializer(planes_disponibles, many=True)
        
        # Devolvemos los planes disponibles con un código 404 y un mensaje clave
        return Response({
            "detail": "No se encontró suscripción activa.",
            "planes_disponibles": serializer.data
        }, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['post'], url_path='confirmar_compra')
    def create_subscription_and_pay(self, request):
        """
        Endpoint: POST /suscripcion/confirmar_compra/
        Recibe el ID del plan, simula el pago, y crea/activa la suscripción.
        """
        serializer = PaymentRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # ...existing code...
        user = request.user
        if not getattr(user, 'is_authenticated', False):
            return Response({'detail': 'Authentication credentials were not provided.'}, status=status.HTTP_401_UNAUTHORIZED)
        # ...existing code...
        tipo_plan = serializer.validated_data['tipo_plan']
        
        # Usamos transaction.atomic para asegurar que todo se guarde o nada se guarde.
        with transaction.atomic():
            # 1. Desactivar suscripciones anteriores (opcional pero recomendado)
            estado_nulo = Estado.objects.get(nombre='nulo')
            Suscripcion.objects.filter(user=user, estado__nombre='activo').update(estado=estado_nulo)
            
            estado_activo = Estado.objects.get(nombre='activo')
            
            # 2. Calcular fechas y características
            fecha_inicio = date.today()
            # Si la duración es 0 (gratuito) o positiva
            if tipo_plan.duracion_mes > 0:
                 fecha_fin = fecha_inicio + timedelta(days=30 * tipo_plan.duracion_mes)
                 dias_restantes = (fecha_fin - fecha_inicio).days
            else:
                 # Plan gratuito o indefinido (ponemos un límite grande o lo manejamos en el front)
                 fecha_fin = fecha_inicio + timedelta(days=36500) # 100 años
                 dias_restantes = 36500

            # 3. Crear la nueva suscripción
            suscripcion = Suscripcion.objects.create(
                user=user,
                estado=estado_activo,
                plan=tipo_plan, 
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin,
                codigo=f'SUB-{uuid.uuid4().hex[:6]}',
                dia_restante=dias_restantes,
                empresa_disponible=tipo_plan.caracteristica.cant_empresas or 999,
                colab_disponible=tipo_plan.caracteristica.cant_colab or 999,
            )
            
            # 4. Simular Pago Ficticio (si el precio es > 0)
            if tipo_plan.precio > 0:
                # Simulamos que la pasarela de pago CONFIRMÓ el pago
                Pago.objects.create(
                    suscripcion=suscripcion,
                    monto=tipo_plan.precio,
                    fecha_pago=date.today(),
                    metodos_pago='tarjeta', # Fijo según la simulación
                    estado_pago='pagado',   # ✅ Simulación: SIEMPRE 'pagado'
                    codigo_pago=f'PAY-{uuid.uuid4().hex[:8]}',
                    id_transaccion_externa='SIMULATED-SUCCESS'
                )
        
        # 5. Respuesta exitosa
        return Response(SubscriptionSuccessSerializer(suscripcion).data, status=status.HTTP_201_CREATED)
