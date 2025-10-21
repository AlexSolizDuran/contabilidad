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
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny


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

class PagoExitosoCallback(APIView):
    # Permite acceso sin autenticación (ya que Libélula te llama directamente)
    permission_classes = [AllowAny] 
    
    def get(self, request):
        """
        Servicio PAGO EXITOSO (Callback de Libélula).
        Libélula llama a esta URL mediante GET después de un pago exitoso.
        Parámetro: transaction_id (identificador_deuda que enviamos)
        """
        transaction_id = request.query_params.get('transaction_id')
        
        if not transaction_id:
            # Respuesta a Libélula: transacción inválida
            return Response({"detail": "Falta el identificador de transacción."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # 1. Buscar la suscripción pendiente usando el identificador_deuda como código
            suscripcion = Suscripcion.objects.get(codigo=transaction_id)
            
            # 2. Verificar si ya fue procesada (para evitar doble pago)
            estado_activo = Estado.objects.get(nombre='activo')
            if suscripcion.estado == estado_activo:
                # Ya estaba activa, simplemente respondemos 200 para Libélula
                return Response({"detail": "Suscripción ya estaba activa."}, status=status.HTTP_200_OK)
            
            # 3. Marcar como pagada y activa
            # Obtenemos el estado 'pagado'
            estado_pagado = Estado.objects.get(nombre='pagado') # Suponiendo que tienes un estado 'pagado' o usamos 'activo'
            
            # En tu implementación, el estado de la suscripción se pone a 'activo'
            suscripcion.estado = estado_activo 
            suscripcion.save()
            
            # 4. Registrar el Pago (usamos los datos que Libélula nos dio en el callback, aunque aquí solo tenemos el ID)
            # En un callback real, Libélula envía más datos que podrías usar para crear el objeto Pago
            
            # Buscamos el tipo de pago (solo para que no falle la creación)
            metodo_pago = 'tarjeta' 
            
            Pago.objects.create(
                suscripcion=suscripcion,
                monto=suscripcion.plan.precio, # Usamos el precio del plan
                fecha_pago=date.today(),
                metodos_pago=metodo_pago,
                estado_pago='pagado',
                codigo_pago=transaction_id,
                id_transaccion_externa=request.query_params.get('invoice_id', 'LIBELULA_WEB')
            )
            
            return Response({"detail": "Pago confirmado y suscripción activada."}, status=status.HTTP_200_OK)

        except Suscripcion.DoesNotExist:
            return Response({"detail": "Deuda no encontrada en el sistema."}, status=status.HTTP_404_NOT_FOUND)
        except Estado.DoesNotExist:
            return Response({"detail": "Error de configuración de estados."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            # Log de cualquier otro error inesperado para revisión
            print(f"Error procesando callback de Libélula: {e}")
            return Response({"detail": "Error interno del servidor al procesar el pago."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)