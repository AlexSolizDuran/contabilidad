import os
from django.http import FileResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

LOG_DIR = "logs"  # Carpeta raíz de logs

class DescargarLogEmpresaView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Descarga el log JSON de un usuario de una empresa específica.
        Solo superusuarios pueden descargar.
        Se espera recibir:
            - empresa_id (query param)
            - usuario_id (query param)
        """
        

        empresa_id = request.query_params.get("empresa_id")
        usuario_id = request.query_params.get("usuario_id")

        if not empresa_id or not usuario_id:
            return Response({"detail": "Faltan parámetros"}, status=status.HTTP_400_BAD_REQUEST)

        archivo = os.path.join(LOG_DIR, empresa_id, f"{usuario_id}.json")

        if not os.path.exists(archivo):
            return Response({"detail": "Archivo no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        return FileResponse(open(archivo, 'rb'), as_attachment=True, filename=f"{usuario_id}.json")
