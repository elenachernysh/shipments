from rest_framework import serializers

from shipments.models import Shipment, Product
from shipments.utils import OptionsMappingField


class ProductListSerializer(serializers.ModelSerializer):

    class Meta:
        fields = (
            "id",
            "title",
            "cost",
        )
        model = Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            "id",
            "title",
            "cost",
        )
        model = Product


class ShipmentListSerializer(serializers.ModelSerializer):
    status = OptionsMappingField(Shipment.DELIVERY_STATUS_CHOICES, default=Shipment.DELIVERY_STATUS_DRAFT)
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects, required=False, write_only=True)

    class Meta:
        fields = (
            "id",
            "title",
            "status",
            "product",
        )
        model = Shipment


class ShipmentSerializer(serializers.ModelSerializer):
    status = OptionsMappingField(Shipment.DELIVERY_STATUS_CHOICES)
    # product = ProductSerializer()  <-- blocked for front-end
    product = serializers.CharField(source='product.title', read_only=True)

    class Meta:
        fields = (
            "id",
            "title",
            "status",
            "description",
            "product",
        )
        model = Shipment
