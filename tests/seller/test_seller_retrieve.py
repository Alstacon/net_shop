import pytest
from django.urls import reverse
from rest_framework import status

from seller.serializers import SellerSerializer
from tests.utils import BaseTestCase


@pytest.mark.django_db
class TestSellerRetrieve(BaseTestCase):
    def test_retrieve_seller_success(self, auth_client, seller_factory):
        seller = seller_factory.create()
        url = reverse('seller:sellers-detail', args=[seller.id])

        response = auth_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == SellerSerializer(seller).data

    def test_retrieve_seller_unauthorized(self, client):
        url = reverse('seller:sellers-detail', args=[1])

        response = client.get(url)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_retrieve_non_active(self, auth_client, non_active_user):
        url = reverse('seller:sellers-detail', args=[1])

        response = auth_client.delete(url, user=non_active_user)

        assert response.status_code == status.HTTP_403_FORBIDDEN
