from django.db import models


class Order(models.Model):
    STATUS_CHOICES = [
        ('NEW', 'new'),
        ('ACCEPTED', 'accepted'),
        ('FAILED', 'failed'),
    ]
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default='NEW', verbose_name='order status')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='order created date in UTC')
    external_id = models.CharField(max_length=128, verbose_name='identifier of the order in external system')

    def __str__(self):
        return self.status


class Product(models.Model):
    name = models.CharField(max_length=64, unique=True, verbose_name='product name')

    def __str__(self):
        return self.name


class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='details', verbose_name='reference to order entity')
    amount = models.PositiveIntegerField(verbose_name='how many items are included in order detail')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='reference to product entity')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='products price')

