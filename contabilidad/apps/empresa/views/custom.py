from rest_framework import viewsets
from ..models import Custom
from ..serializers import (CustomCreateSerializer,
                                      CustomDetailSerializer,
                                      CustomListSerializer)


class CustomViewSet(viewsets.ModelViewSet):
    queryset = Custom.objects.all()
    serializer_class = CustomListSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return CustomListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return CustomCreateSerializer
        elif self.action in ['retrieve', 'destroy']:
            return CustomDetailSerializer
        return super().get_serializer_class()