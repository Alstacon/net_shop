from rest_framework import viewsets
import django_filters.rest_framework
from seller.models import Seller
from seller.permissions import IsActive
from seller.serializers import SellerSerializer, SellerCreateSerializer, SellerUpdateSerializer


class SellerViewSet(viewsets.ModelViewSet):
    default_queryset = Seller.objects.all()
    default_serializer_class = SellerSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, ]
    filterset_fields = ['country']

    permission_classes = [IsActive]

    querysets = {
        'list': Seller.objects.prefetch_related('products').all(),
    }

    serializers = {
        'create': SellerCreateSerializer,
        'update': SellerUpdateSerializer,
        'partial_update': SellerUpdateSerializer,
    }

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.default_serializer_class)

    def get_queryset(self):
        return self.querysets.get(self.action, self.default_queryset)
