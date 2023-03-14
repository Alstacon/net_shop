import pytest
from django.urls import reverse
from rest_framework import status

from seller.models import Seller
from tests.utils import BaseTestCase


@pytest.mark.django_db
class TestSellerUpdate(BaseTestCase):
    def test_update_seller_success(self, auth_client, seller_factory):
        seller = seller_factory.create()
        url = reverse('seller:sellers-detail', args=[seller.id])

        response = auth_client.patch(url, data={'title': 'New title'})

        assert response.status_code == status.HTTP_200_OK

        seller.refresh_from_db()

        assert seller.title == 'New title'

    def test_update_to_factory(self, auth_client, seller_factory):
        seller_provider = seller_factory.create(type=1)

        seller_buyer = seller_factory.create(type=2, provider=seller_provider)

        assert seller_buyer.type == Seller.SellerType.retailer
        assert seller_buyer.level == 1
