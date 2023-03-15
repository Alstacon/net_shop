import pytest
from django.urls import reverse
from rest_framework import status

from seller.models import Seller
from tests.utils import BaseTestCase


@pytest.mark.django_db
class TestSellerDelete(BaseTestCase):
    def test_delete_seller_success(self, auth_client, seller_factory):
        seller = seller_factory.create()

        assert Seller.objects.last()

        url = reverse('seller:sellers-detail', args=[seller.id])

        response = auth_client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Seller.objects.last()

    def test_delete_unauthorized(self, client):
        url = reverse('seller:sellers-detail', args=[1])

        response = client.delete(url)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_non_active(self, auth_client, non_active_user):
        url = reverse('seller:sellers-detail', args=[1])

        response = auth_client.delete(url, user=non_active_user)

        assert response.status_code == status.HTTP_403_FORBIDDEN
