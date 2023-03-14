import pytest
from django.urls import reverse
from rest_framework import status

from seller.serializers import SellerSerializer
from tests.utils import BaseTestCase


@pytest.mark.django_db
class TestSellerList(BaseTestCase):
    url = reverse('seller:sellers-list')

    def test_get_list(self, auth_client, seller_factory):
        sellers = seller_factory.create_batch(2)

        response = auth_client.get(self.url)

        assert response.status_code == status.HTTP_200_OK
        for seller in SellerSerializer(sellers, many=True).data:
            assert seller in response.data

    def test_country_filter(self, auth_client, seller_factory, faker):
        seller_factory.create_batch(6)
        country = faker.country()
        params = {'country': country}

        seller_factory.create_batch(2, country=country)

        response = auth_client.get(self.url, params)
        assert response.status_code == status.HTTP_200_OK

        assert len(response.json()) == 2

    def test_list_unauthorized(self, client):
        response = client.get(self.url)

        assert response.status_code == status.HTTP_403_FORBIDDEN
