from django.db import transaction
from rest_framework import serializers

from seller.models import Seller, Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class SellerSerializer(serializers.ModelSerializer):
    type = serializers.ChoiceField(required=True, choices=Seller.SellerType.choices)
    provider = 'SellerSerializer(read_only=True, required=False)'
    products = ProductSerializer(many=True)

    class Meta:
        model = Seller
        fields = '__all__'
        read_only_fields = ('id', 'created', 'debt')


class SellerCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    products = ProductSerializer(many=True, required=False)

    class Meta:
        model = Seller
        fields = '__all__'
        read_only_fields = ('id', 'created')

    def is_valid(self, *, raise_exception=False):
        self._products = self.initial_data.pop('products')
        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        validated_data.pop('user')
        seller = Seller.objects.create(**validated_data)

        for product in self._products:
            product['seller'] = Seller.objects.get(id=product['seller'])
            product = Product.objects.create(**product)
            seller.products.add(product)

        seller.save()
        return seller


class SellerUpdateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    products = ProductSerializer(many=True, required=False)

    class Meta:
        model = Seller
        fields = '__all__'
        read_only_fields = ('id', 'created', 'debt')

    def update(self, instance: Seller, validated_data: dict) -> Seller:
        """Удаляет из списка все продукты и записывает заново."""
        with transaction.atomic():
            Product.objects.filter(seller=instance).delete()
            Product.objects.bulk_create([
                Product(
                    title=product['title'],
                    model=product['model'],
                    released=product['released'],
                    seller=instance,
                )
                for product in validated_data.pop('products', [])
            ])

            super().update(instance, validated_data)

        return instance
