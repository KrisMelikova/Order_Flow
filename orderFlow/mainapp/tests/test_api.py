from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, RequestsClient

from mainapp.models import Order, Product, OrderDetail


class ApiTestCase(APITestCase):

    def setUp(self):
        self.product_1 = Product.objects.create(id=4, name="Dropbox")
        self.order_1 = Order.objects.create(id=1, status="NEW", created_at=None, external_id="QWE-456")
        self.order_1_detail = OrderDetail.objects.create(id=1, order=self.order_1, product=self.product_1, amount=10,
                                                         price=12.00)

    def test_get_request(self):
        expecting_data = {
            "items_count": 1,
            "next item": None,
            "previous item": None,
            "items": [{
                "id": 1,
                "status": "NEW",
                "created_at": None,
                "external_id": "QWE-456",
                "details": [{
                    "id": 1,
                    "amount": 10,
                    "product": {"id": 4,
                                "name": "Dropbox"},
                    "price": '12.00'
                }]
            }]
        }

        url = reverse("order-list")
        response = self.client.get(url, format='json')
        expecting_data["items"][0]["created_at"] = response.data["items"][0]["created_at"]
        self.assertEqual(200, response.status_code)
        self.assertEqual(expecting_data, response.data)

    def test_get_detail_of_order(self):
        expecting_data = {
            "id": 1,
            "status": "NEW",
            "created_at": None,
            "external_id": "QWE-456",
            "details": [{
                "id": 1,
                "amount": 10,
                "product": {"id": 4,
                            "name": "Dropbox"},
                "price": '12.00'
            }]
        }
        client = RequestsClient()
        response = client.get('http://testserver/api/v1/orders/1')
        expecting_data["created_at"] = response.json()["created_at"]
        assert response.status_code == 200
        self.assertEqual(response.json(), expecting_data)

    def test_post_request(self):
        data = {
            "external_id": "PR-123-321-123",
            "details": [{
                "product": {"id": 4},
                "amount": 10,
                "price": "12.00"
            }]
        }
        expecting_data = {
            "id": 2,
            "status": "NEW",
            "created_at": None,
            "external_id": "PR-123-321-123",
            "details": [{
                "id": 2,
                "amount": 10,
                "product": {"id": 4,
                            "name": "Dropbox"},
                "price": '12.00'
            }]
        }

        url = reverse('order-list')
        response = self.client.post(url, data, format='json')
        expecting_data["created_at"] = response.data["created_at"]
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 2)
        self.assertEqual(expecting_data, response.data)

    def test_create_order_with_wrong_product_id(self):
        data = {
            "external_id": "PR-123-321-123",
            "details": [{
                "product": {"id": 10},
                "amount": 10,
                "price": "12.00"
            }]
        }

        url = reverse('order-list')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 404)

    def test_create_order_without_details(self):
        data = {
            "external_id": "PR-123-321-123"
        }

        url = reverse('order-list')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_partial_update(self):
        order_with_changes = {
            "status": "accepted",
            "external_id": "QWE-123-yui-YUI-3453"
        }
        expecting_order_info = {
            "id": 1,
            "status": "NEW",
            "created_at": None,
            "external_id": "QWE-123-yui-YUI-3453",
            "details": [{
                "id": 1,
                "amount": 10,
                "product": {"id": 4,
                            "name": "Dropbox"},
                "price": '12.00'
            }]
        }

        client = RequestsClient()
        response = client.put('http://testserver/api/v1/orders/1', order_with_changes)
        expecting_order_info["created_at"] = response.json()["created_at"]
        self.assertEqual(expecting_order_info, response.json())
        self.assertEqual(response.status_code, 200)

    def test_dont_update_with_status_accepted(self):
        product_2 = Product.objects.create(id=5, name="Google Drive")
        order_2 = Order.objects.create(id=2, status="accepted", created_at=None, external_id="PPP-HHH555")
        order_2_detail = OrderDetail.objects.create(id=3, order=order_2, product=product_2, amount=5, price=13.00)
        order_with_changes = {
            "external_id": "JJJ-999-KKK"
        }

        client = RequestsClient()
        response = client.put('http://testserver/api/v1/orders/2', order_with_changes)
        self.assertEqual(response.status_code, 403)

    def test_destroy(self):
        client = RequestsClient()
        response = client.delete('http://testserver/api/v1/orders/1')
        self.assertEqual(response.status_code, 204)

    def test_destroy_accepted(self):
        product_2 = Product.objects.create(id=5, name="Google Drive")
        order_2 = Order.objects.create(id=2, status="accepted", created_at=None, external_id="PPP-HHH555")
        order_2_detail = OrderDetail.objects.create(id=3, order=order_2, product=product_2, amount=5, price=13.00)

        client = RequestsClient()
        response = client.delete('http://testserver/api/v1/orders/2')
        self.assertEqual(response.status_code, 403)

    def test_status_accepted(self):
        data = {}

        response = self.client.post('http://testserver/api/v1/orders/1/accepted', data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, 'accepted')

    def test_status_fail(self):
        data = {}

        response = self.client.post('http://testserver/api/v1/orders/1/fail', data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, 'rejected')












