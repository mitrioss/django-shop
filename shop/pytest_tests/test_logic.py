from pytest_django.asserts import assertRedirects
from shop.models import Review
from orders.models import Order
from django.urls import reverse
import pytest
from unittest.mock import patch


def test_user_can_create_review(user, user_client, prod, rev_data):
    url = reverse('shop:product_detail', args=[prod.id, prod.slug])
    response = user_client.post(url, data=rev_data)
    assertRedirects(response, url)
    review = Review.objects.filter(product=prod, user=user).first()
    assert review is not None
    assert review.rating == 5


def test_user_cant_create_blank_review(user, user_client, prod):
    url = reverse('shop:product_detail', args=[prod.id, prod.slug])
    response = user_client.post(url, data={})
    assert response.status_code == 200
    review = Review.objects.all().first()
    assert review is None




def test_anonymous_user_cant_create_review(user, client, prod, rev_data):
    url = reverse('shop:product_detail', args=[prod.id, prod.slug])
    response = client.post(url, data=rev_data)
    assertRedirects(response, reverse('login'))


@pytest.mark.django_db
@patch('orders.views.order_created.delay')  # Мокируем Celery-задачу
def test_order_create(user, user_client, prod, order_data, django_user_model):
    user = django_user_model.objects.create(username='testuser')
    user_client.force_login(user)

    session = user_client.session
    session['cart'] = {prod.id: {'quantity': 1, 'price': prod.price}}
    session.save()

    url = reverse('orders:order_create')
    response = user_client.post(url, data=order_data)
    assertRedirects(response, reverse('payment:process'))
    order = Order.objects.filter(email='johndoe@example.com').first()
    assert order is not None


@pytest.mark.django_db
@patch('orders.views.order_created.delay')
def test_order_create_empty_cart(mock_order_created, client, user, order_data):
    client.force_login(user)

    session = client.session
    session['cart'] = {}
    session.save()

    url = reverse('orders:order_create')
    response = client.post(url, data=order_data)

    assertRedirects(response, reverse('cart:cart_detail'))
    mock_order_created.assert_not_called()
