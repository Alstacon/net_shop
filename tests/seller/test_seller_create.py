import pytest
from django.urls import reverse
from rest_framework import status

from seller.models import Seller
from seller.serializers import SellerSerializer
from tests.utils import BaseTestCase


@pytest.mark.django_db
class TestSellerCreate(BaseTestCase):
    url = reverse('seller:sellers-list')

    def test_create_success(self, auth_client):
        response = auth_client.post(self.url, data={
            'type': 1,
            'title': 'Завод',
            'email': 'pp@mail.ru',
            'country': '-',
            'city': '-',
            'street': '-',
            'building': '-',
        })

        seller = Seller.objects.last()

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json() == SellerSerializer(seller).data

    def test_create_unauthorized(self, client, faker):
        response = client.post(self.url, data=faker.pydict(1))

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_create_invalid_data(self, auth_client, faker):
        response = auth_client.post(self.url, data={
            'type': 1,
            'email': 'pp@mail.ru',
            'country': '-',
            'city': '-',
            'street': '-',
            'building': '-',
        })

        assert response.status_code == status.HTTP_400_BAD_REQUEST

        assert not Seller.objects.last()

    def test_create_factory(self, auth_client):
        response = auth_client.post(self.url, data={
            'type': 1,
            'title': 'Завод',
            'email': 'pp@mail.ru',
            'country': '-',
            'city': '-',
            'street': '-',
            'building': '-',
        })

        assert response.status_code == status.HTTP_201_CREATED

        seller = Seller.objects.last()

        assert seller.level == 0
        assert seller.provider is None

    def test_create_non_factory_with_provider(self, auth_client):
        auth_client.post(self.url, data={
            'type': 1,
            'title': 'Завод',
            'email': 'pp@mail.ru',
            'country': '-',
            'city': '-',
            'street': '-',
            'building': '-',
        })

        factory = Seller.objects.last()
        assert factory.level == 0

        response = auth_client.post(self.url, data={
            'type': 2,
            'title': 'Еще завод',
            'email': 'pp@mail.ru',
            'country': '-',
            'city': '-',
            'street': '-',
            'building': '-',
            'provider': factory.id
        })

        assert response.status_code == status.HTTP_201_CREATED

        buyer = Seller.objects.last()

        assert buyer.level == 1

    def test_create_non_active(self, auth_client, non_active_user, faker, ):
        response = auth_client.post(self.url, data=faker.pydict(1), user=non_active_user)

        assert response.status_code == status.HTTP_403_FORBIDDEN
