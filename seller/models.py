from django.db import models


class Seller(models.Model):
    class SellerType(models.IntegerChoices):
        factory = 1, 'Завод',
        retailer = 2, 'Розничная сеть',
        entrepreneur = 3, 'Индивидуальный предприниматель'

    type = models.PositiveSmallIntegerField(choices=SellerType.choices, default=SellerType.factory,
                                            verbose_name='Тип продавца')
    level = models.PositiveSmallIntegerField(default=0, verbose_name='Уровень в иерархии')
    title = models.CharField(max_length=255, verbose_name='Название')
    provider = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, verbose_name='Поставщик',
                                 related_name='seller')
    email = models.EmailField(max_length=100, verbose_name='Email')
    country = models.CharField(max_length=50, verbose_name='Страна')
    city = models.CharField(max_length=50, verbose_name='Город')
    street = models.CharField(max_length=50, verbose_name='Улица')
    building = models.CharField(max_length=10, verbose_name='Номер дома')
    debt = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Задолженность перед поставщиком')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')

    class Meta:
        verbose_name = 'Продавец'
        verbose_name_plural = 'Продавцы'

    def __str__(self):
        return f'{self.title}'


class Product(models.Model):
    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, verbose_name='Продавец', related_name='products')
    title = models.CharField(max_length=255, verbose_name='Название')
    model = models.CharField(max_length=255, verbose_name='Модель')
    released = models.DateField(verbose_name='Дата выхода продукта на рынок')
