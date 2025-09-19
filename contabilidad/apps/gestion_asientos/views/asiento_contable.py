from rest_framework import viewsets
from ..models.asiento_contable import AsientoContable
from ..serializers.asiento_contable import AsientoContableSerializer
from rest_framework.permissions import IsAuthenticated

class AsientoContableViewSet(viewsets.ModelViewSet):
    queryset = AsientoContable.objects.all()
    serializer_class = AsientoContableSerializer
    permission_classes = [IsAuthenticated]
    def create(self, request, *args, **kwargs):
        print("Payload recibido:", request.data)  # 👈 aquí ves el JSON que envía el frontend
        return super().create(request, *args, **kwargs)
    