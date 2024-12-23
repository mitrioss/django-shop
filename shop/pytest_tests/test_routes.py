from http import HTTPStatus
import pytest
from django.urls import reverse
from pytest_django.fixtures import client



@pytest.mark.django_db
@pytest.mark.parametrize(
    'name',
    ['shop:product_list', 'cart:cart_detail'],
    ids=['Список товаров', 'Корзина']
)
def test_pages_availability_for_anonymous_user(client, name):
    url = reverse(name)
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'name',
    ['user:profile']
)
def test_pages_availability_for_auth_user(client, user, name):
    client.force_login(user)
    url = reverse(name)
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
@pytest.mark.parametrize(
    'name',
    ['shop:product_detail']
)
def test_prod_exists(client, prod, name):
    url = reverse(name, kwargs={'id': prod.id, 'slug': prod.slug})
    response = client.post(url)
    assert response.status_code == 302

