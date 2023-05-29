from django.urls import re_path
from shipments.views import ShippingListView, ShippingDetailView, ProductsListView, ProductDetailView


urlpatterns = [
    re_path(r'^$', ShippingListView.as_view(), name='shipping'),
    re_path(r'^(?P<pk>[0-9]+)/$', ShippingDetailView.as_view(), name='shipping_detail'),
    re_path(r'^product/', ProductsListView.as_view(), name='product'),
    re_path(r'^product/(?P<pk>[0-9]+)/$', ProductDetailView.as_view(), name='product_detail'),
]
