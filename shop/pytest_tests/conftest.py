import pytest
from django.test.client import Client
import os
import django
from shop.models import *


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myshop.settings")
django.setup()


@pytest.fixture
def user(django_user_model):
    user = django_user_model.objects.create(username='Тестовый пользователь')
    return user


@pytest.fixture
def unlog_client():
    client = Client()
    return client


@pytest.fixture
def admin_user(django_user_model):
    admin = django_user_model.objects.create_superuser(username='Тестовый администратор')
    return admin


@pytest.fixture
def user_client(user):
    client = Client()
    client.force_login(user)
    return client


@pytest.fixture
def prod():
    categ = Category.objects.create(
        name='Europe',
        slug='Europe'
    )
    prod = Product.objects.create(
        slug='test1-slug',
        category=categ,
        name = 'test1',
        price = 111,
    )
    return prod


@pytest.fixture
def review(user, prod):
    rev = Review.objects.create(
        product=prod,
        user=user,
        rating=5,
    )
    return rev


@pytest.fixture
def rev_data():
    return {
        'rating': 5,
        'comment': 'Отличный продукт!'
    }


@pytest.fixture
def order_data():
    return {
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'johndoe@example.com',
        'address': '123 Test St',
        'postal_code': '12345',
        'city': 'Testville',
    }

