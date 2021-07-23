import pytest

from rest_framework.reverse import reverse
from rest_framework import status

from rest_framework.test import RequestsClient, APIClient

from mainapp.models import Order, Product, OrderDetail


@pytest.fixture
def example_data():
    product_1 = Product.objects.create(id=4, name="Dropbox")
    order_1 = Order.objects.create(id=1, status="NEW", created_at=None, external_id="QWE-456")
    order_1_detail = OrderDetail.objects.create(id=1, order=order_1, product=product_1, amount=10, price=12.00)
    return order_1_detail


@pytest.fixture
def example_data_status_accepted():
    product_2 = Product.objects.create(id=5, name="Google Drive")
    order_2 = Order.objects.create(id=2, status="accepted", created_at=None, external_id="PPP-HHH555")
    order_2_detail = OrderDetail.objects.create(id=3, order=order_2, product=product_2, amount=5, price=13.00)
    return order_2_detail


@pytest.mark.django_db
def test_get_request(example_data):
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

    client = RequestsClient()
    response = client.get('http://testserver/api/v1/orders')
    expecting_data["items"][0]["created_at"] = response.json()["items"][0]["created_at"]
    assert response.status_code == 200
    assert expecting_data == response.json()


@pytest.mark.django_db
def test_get_detail_of_order(example_data):
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
    assert expecting_data == response.json()


@pytest.mark.django_db
def test_post_request(example_data):
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

    client = APIClient()
    url = reverse('order-list')
    response = client.post(url, data, format='json')
    expecting_data["created_at"] = response.data["created_at"]
    assert response.status_code == status.HTTP_201_CREATED
    assert Order.objects.count() == 2
    assert expecting_data == response.data


@pytest.mark.django_db
def test_create_order_with_wrong_product_id():
    data = {
        "external_id": "PR-123-321-123",
        "details": [{
            "product": {"id": 10},
            "amount": 10,
            "price": "12.00"
        }]
    }

    client = APIClient()
    url = reverse('order-list')
    response = client.post(url, data, format='json')
    assert response.status_code == 404


@pytest.mark.django_db
def test_create_order_without_details():
    data = {
        "external_id": "PR-123-321-123"
    }

    client = APIClient()
    url = reverse('order-list')
    response = client.post(url, data, format='json')
    assert response.status_code == 400


@pytest.mark.django_db
def test_partial_update(example_data):
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

    client = APIClient()
    response = client.put('http://testserver/api/v1/orders/1', order_with_changes)
    expecting_order_info["created_at"] = response.json()["created_at"]
    assert expecting_order_info == response.json()
    assert response.status_code == 200


@pytest.mark.django_db
def test_dont_update_with_status_accepted(example_data_status_accepted):
    order_with_changes = {
        "external_id": "JJJ-999-KKK"
    }

    client = APIClient()
    response = client.put('http://testserver/api/v1/orders/2', order_with_changes)
    assert response.status_code == 403


@pytest.mark.django_db
def test_destroy(example_data):
    client = RequestsClient()
    response = client.delete('http://testserver/api/v1/orders/1')
    assert response.status_code == 204


@pytest.mark.django_db
def test_destroy_accepted(example_data_status_accepted):
    client = RequestsClient()
    response = client.delete('http://testserver/api/v1/orders/2')
    assert response.status_code == 403


@pytest.mark.django_db
def test_status_accepted(example_data):
    data = {}

    client = APIClient()
    response = client.post('http://testserver/api/v1/orders/1/accepted', data, format='json')
    assert response.status_code == 200
    assert response.data == 'accepted'


@pytest.mark.django_db
def test_status_fail(example_data):
    data = {}

    client = APIClient()
    response = client.post('http://testserver/api/v1/orders/1/fail', data, format='json')
    assert response.status_code == 200
    assert response.data == 'rejected'




