from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    title = models.CharField(max_length=50)
    cost = models.IntegerField()


class Shipment(models.Model):
    DELIVERY_STATUS_DRAFT = 0
    DELIVERY_STATUS_PUBLISHED = 1
    DELIVERY_STATUS_STAGED = 2
    DELIVERY_STATUS_DONE = 3
    DELIVERY_STATUS_DECLINED = 4

    DELIVERY_STATUS_CHOICES = (
        (DELIVERY_STATUS_DRAFT, 'draft'),
        (DELIVERY_STATUS_PUBLISHED, 'published'),
        (DELIVERY_STATUS_STAGED, 'staged'),
        (DELIVERY_STATUS_DONE, 'done'),
        (DELIVERY_STATUS_DECLINED, 'declined'),
    )

    title = models.CharField(max_length=50)
    product = models.ForeignKey(Product, blank=True, null=True, on_delete=models.CASCADE, related_name='product')
    status = models.IntegerField(choices=DELIVERY_STATUS_CHOICES, default=DELIVERY_STATUS_DRAFT)
    description = models.CharField(max_length=150)
    created_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['id']
