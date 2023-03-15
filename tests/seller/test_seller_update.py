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

        seller_buyer = seller_factory.create(title='Покупатель', type=2, level=1, provider=seller_provider)

        assert seller_buyer.type == Seller.SellerType.retailer
        assert seller_buyer.level == 1

        url = reverse('seller:sellers-detail', args=[seller_buyer.id])

        response = auth_client.patch(url, data={'type': 1})

        assert response.status_code == status.HTTP_200_OK
        seller_buyer.refresh_from_db()

        assert seller_buyer.title == 'Покупатель'
        assert seller_buyer.type == Seller.SellerType.factory
        assert seller_buyer.level == 0

    def test_update_to_factory_with_buyers(self, auth_client, seller_factory):
        seller_provider = seller_factory.create(type=1)

        seller_buyer = seller_factory.create(title='Покупатель', type=2, level=1, provider=seller_provider)
        seller_lower_buyer = seller_factory.create(title='Покупатель 2', type=3, level=2, provider=seller_buyer)
        seller_last_buyer = seller_factory.create(title='Покупатель 3', type=2, level=3, provider=seller_lower_buyer)

        assert seller_buyer.type == Seller.SellerType.retailer
        assert seller_buyer.level == 1

        url = reverse('seller:sellers-detail', args=[seller_buyer.id])

        response = auth_client.patch(url, data={'type': 1})

        assert response.status_code == status.HTTP_200_OK
        seller_buyer.refresh_from_db()
        seller_lower_buyer.refresh_from_db()
        seller_last_buyer.refresh_from_db()

        assert seller_buyer.title == 'Покупатель'
        assert seller_buyer.type == Seller.SellerType.factory
        assert seller_buyer.level == 0

        assert seller_lower_buyer.title == 'Покупатель 2'
        assert seller_lower_buyer.type == Seller.SellerType.entrepreneur
        assert seller_lower_buyer.level == 1

        assert seller_last_buyer.title == 'Покупатель 3'
        assert seller_last_buyer.type == Seller.SellerType.retailer
        assert seller_last_buyer.level == 2

    def test_cant_update_debt(self, auth_client, seller_factory):
        seller = seller_factory.create(type=1)
        url = reverse('seller:sellers-detail', args=[seller.id])

        seller_debt = seller.debt
        response = auth_client.patch(url, data={'debt': '100.00'})

        assert response.status_code == status.HTTP_200_OK

        seller.refresh_from_db()
        assert seller.debt == seller_debt and seller_debt != '100.00'

    def test_update_unauthorized(self, client, faker, seller_factory):
        seller = seller_factory.create()

        url = reverse('seller:sellers-detail', args=[seller.id])
        response = client.patch(url, data=faker.pydict(1))

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_update_non_active(self, auth_client, non_active_user, seller_factory):
        seller = seller_factory.create()

        url = reverse('seller:sellers-detail', args=[seller.id])
        response = auth_client.delete(url, user=non_active_user)

        assert response.status_code == status.HTTP_403_FORBIDDEN
