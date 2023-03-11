from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from seller.models import Seller, Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class SellerSerializer(serializers.ModelSerializer):
    type = serializers.ChoiceField(required=True, choices=Seller.SellerType.choices)
    provider = 'SellerSerializer(read_only=True, required=False)'
    products = ProductSerializer(many=True)
    buyers = 'SellerSerializer(read_only=True, required=False, many=True)'

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

    def create(self, validated_data: dict) -> Seller:
        validated_data.pop('user')
        seller = Seller.objects.create(**validated_data)

        if seller.type == Seller.SellerType.factory:
            seller.level = 0
        else:
            if seller.provider:
                seller.level = seller.provider.level + 1

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
        """Удаляет из списка все продукты и записывает заново с изменения."""
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

            if instance.type == Seller.SellerType.factory:
                instance.level = 0
                instance.provider = None
                Seller.objects.filter(provider=instance).update(level=1)
            else:
                if instance.provider:
                    if instance.provider == instance:
                        raise ValidationError('Выберите другого поставщика.')
                    instance.level = instance.provider.level + 1
                    instance.save()
                    Seller.objects.filter(provider=instance).update(level=instance.level + 1)

        return instance
