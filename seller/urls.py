from django.urls import path, include
from rest_framework.routers import SimpleRouter

from seller.views import SellerViewSet

router = SimpleRouter()

router.register('seller', SellerViewSet, basename='sellers')

urlpatterns = [
    path('', include(router.urls)),
]
