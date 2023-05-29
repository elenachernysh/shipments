import factory

from shipments.models import Shipment,Product


class ProductFactory(factory.django.DjangoModelFactory):
    title = 'dummy title'
    cost = '100'

    class Meta:
        model = Product


class ShipmentFactory(factory.django.DjangoModelFactory):
    product = factory.SubFactory(ProductFactory)

    class Meta:
        model = Shipment
