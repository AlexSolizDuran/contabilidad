from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from ..models import Favorito
from ..serializers import FavoritoListSerializer, FavoritoCreateSerializer
from .user_empresa import UserEmpresa

class FavoritoAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        empresa = request.auth.get('empresa')
        user_empresa = UserEmpresa.objects.get(usuario=user, empresa=empresa)
        favoritos = Favorito.objects.filter(user_empresa=user_empresa)
        serializer = FavoritoListSerializer(favoritos, many=True)
        return Response(serializer.data)

    def post(self, request):
        user = request.user
        empresa = request.auth.get('empresa')
        user_empresa = UserEmpresa.objects.get(usuario=user, empresa=empresa)
        serializer = FavoritoCreateSerializer(data=request.data)
        if serializer.is_valid():
            # Guardamos el favorito con la relación al user_empresa
            serializer.save(user_empresa=user_empresa)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



    def delete(self, request, pk=None):
        """Eliminar favorito por id (recibido en la URL)"""
        if not pk:
            return Response({"detail": "Se requiere el ID del favorito"}, status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        empresa = request.auth.get('empresa')
        user_empresa = UserEmpresa.objects.get(usuario=user, empresa=empresa)
        favorito = Favorito.objects.filter(user_empresa=user_empresa, id=pk).first()
        if favorito:
            favorito.delete()
            return Response({"detail": "Eliminado"})
        return Response({"detail": "No encontrado"}, status=status.HTTP_404_NOT_FOUND)
