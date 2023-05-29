from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from shipments.models import Shipment, Product
from shipments.serializers import ShipmentSerializer, ShipmentListSerializer, ProductListSerializer, ProductSerializer
from shipments.utils import CustomPagination, SimpleTextSearchMixin


class ShippingListView(SimpleTextSearchMixin, generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Shipment.objects.all()
    serializer_class = ShipmentListSerializer
    pagination_class = CustomPagination

    search_fields = (
        'title',
        'product__title',
    )

    def get_queryset(self):
        queryset = super().get_queryset()

        filtered_queryset = self.convert_search_to_simple_search(
            queryset,
            self.search_fields
        )
        return filtered_queryset


class ShippingDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Shipment.objects.all()
    serializer_class = ShipmentSerializer


class ProductsListView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    pagination_class = CustomPagination


class ProductDetailView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Product.objects.all()
    serializer_class = ProductSerializer