from django.urls import path, include
from rest_framework import routers

from .api_views import ProductListAPIView, ProductPutDeleteListAPIView, OrderViewSet

router = routers.SimpleRouter(trailing_slash=False)
router.register('orders', OrderViewSet)
router.register('orders/', OrderViewSet)

urlpatterns = [
    path('products/', ProductListAPIView.as_view(), name='products_list'),
    path('products/<int:pk>', ProductPutDeleteListAPIView.as_view(), name='product'),
    path('', include(router.urls))
]


