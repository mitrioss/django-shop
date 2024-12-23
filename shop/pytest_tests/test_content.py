from http import HTTPStatus
import pytest
from django.urls import reverse
from pytest_django.fixtures import client
from shop.forms import ReviewForm, Review


def test_create_review(client, user, review, prod, rev_data):
    url = reverse('shop:product_detail', args=[prod.id, prod.slug])
    response = client.get(url)
    assert 'form' in response.context
    assert isinstance(response.context['review_form'], ReviewForm)


@pytest.mark.django_db
def test_cart_display(user_client, prod):
    # Аутентификация пользователя

    session = user_client.session
    session['cart'] = {prod.id: {'quantity': 1, 'price': prod.price}}
    session.save()

    url = reverse('cart:cart_detail')
    response = user_client.get(url)
    assert response.status_code == 200
    assert prod.name in response.content.decode('utf-8')














