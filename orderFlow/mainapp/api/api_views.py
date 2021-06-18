from collections import OrderedDict

from rest_framework import viewsets, status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.decorators import action


from .serializers import OrderSerializer, ProductSerializer
from ..models import Order, Product


# Pagination settings
class MyLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 3

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('items_count', self.count),
            ('next item', self.get_next_link()),
            ('previous item', self.get_previous_link()),
            ('items', data)
        ]))


# Create 'products/' for correct work of web application (it helps to fill, see, update  and delete products)
# GET, POST methods for products/
class ProductListAPIView(ListCreateAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    pagination_class = MyLimitOffsetPagination


# PUT, DELETE methods for products/
class ProductPutDeleteListAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    pagination_class = MyLimitOffsetPagination

    # Make status 'accepted'
    @action(detail=True, methods=['post'])
    def accepted(self, request, pk=None):
        order = Order.objects.get(id=pk)
        order.status = "accepted"
        order.save()
        return Response(order.status)

    # Make status 'rejected'
    @action(detail=True, methods=['post'])
    def fail(self, request, pk=None):
        order = Order.objects.get(id=pk)
        order.status = "rejected"
        order.save()
        return Response(order.status)

    # Delete order if it doesn't have status "accepted"
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.status == "accepted":
            return Response("Order with status 'accepted' can't be deleted", status=status.HTTP_403_FORBIDDEN)
        return super(OrderViewSet, self).destroy(request, *args, **kwargs)









