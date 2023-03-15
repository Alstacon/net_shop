import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from pytest_factoryboy import register

from tests.factories import SellerFactory

register(SellerFactory)


@pytest.fixture()
def client() -> APIClient:
    return APIClient()


@pytest.fixture()
def auth_client(client, user) -> APIClient:
    client.force_login(user)
    return client


@pytest.fixture()
def user():
    return User.objects.create_user(username='lauren')


@pytest.fixture()
def non_active_user(user):
    user.is_active = False
    user.save()
    return user
