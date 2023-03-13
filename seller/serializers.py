from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from seller.models import Seller, Product
from seller.tools import update_level_obj


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

    def create(self, validated_data: dict) -> Seller:
        validated_data.pop('user')
        products = validated_data.pop('products', [])
        seller = Seller.objects.create(**validated_data)

        if seller.type == Seller.SellerType.factory:
            seller.level = 0
        else:
            if seller.provider:
                seller.level = seller.provider.level + 1

        for item in products:
            product, _ = Product.objects.get_or_create(
                title=item['title'],
                model=item['model'],
                released=item['released'],
            )
            seller.products.add()

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
        with transaction.atomic():
            if 'products' in validated_data:
                instance.products.clear()
                if products := validated_data.pop('products'):
                    for item in products:
                        product, _ = Product.objects.get_or_create(
                            title=item['title'],
                            model=item['model'],
                            released=item['released'],
                        )
                        instance.products.add(product)

            super().update(instance, validated_data)

            if instance.type == Seller.SellerType.factory:
                instance.level = 0
                instance.provider = None
                instance.save()
                update_level_obj(instance)
            else:
                if instance.provider:
                    if instance.provider == instance:
                        raise ValidationError('Выберите другого поставщика.')
                    instance.level = instance.provider.level + 1
                    instance.save()
                    update_level_obj(instance)

        return instance
