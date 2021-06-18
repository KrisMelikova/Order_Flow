from rest_framework import serializers
from rest_framework.exceptions import NotFound, ParseError, PermissionDenied

from django.core.exceptions import ObjectDoesNotExist

from ..models import Order, OrderDetail, Product


class ProductSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    name = serializers.CharField(max_length=100, required=False)

    class Meta:
        model = Product
        fields = ['id', 'name']


class OrderDetailSerializer(serializers.ModelSerializer):
    amount = serializers.IntegerField()
    product = ProductSerializer()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = OrderDetail
        fields = ['id', 'amount', 'product', 'price']


class OrderSerializer(serializers.ModelSerializer):
    status = serializers.CharField(required=False)
    created_at = serializers.DateTimeField(required=False)
    external_id = serializers.CharField(required=False)
    details = OrderDetailSerializer(many=True, required=False)

    class Meta:
        model = Order
        fields = ['id', 'status', 'created_at', 'external_id', 'details']

    # Writing 'details' field
    def create(self, validated_data):
        details_data = validated_data.pop('details', [])
        order = Order.objects.create(**validated_data)
        if not details_data:
            raise ParseError
        for detail_data in details_data:
            product_data = detail_data.pop('product')
            try:
                product = Product.objects.get(id=product_data['id'])
            except ObjectDoesNotExist:
                raise NotFound("Product does not exist")
            OrderDetail.objects.create(order=order, product=product, **detail_data)
        return order

    # Modifying update (users should only be able to update the 'external_id' field for an Order if order
    # doesnt have status 'accepted')
    def update(self, instance, validated_data):
        if instance.status == "accepted":
            raise PermissionDenied
        instance.external_id = validated_data.get('external_id', instance.external_id)
        instance.save()
        return instance