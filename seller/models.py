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
    provider = models.OneToOneField('self', on_delete=models.PROTECT, null=True, blank=True, verbose_name='Поставщик',
                                    related_name='seller')
    email = models.EmailField(max_length=100, null=True, blank=True, verbose_name='Email')
    country = models.CharField(max_length=100, null=True, blank=True, verbose_name='Страна')
    city = models.CharField(max_length=100, null=True, blank=True, verbose_name='Город')
    street = models.CharField(max_length=100, null=True, blank=True, verbose_name='Улица')
    building = models.CharField(max_length=10, null=True, blank=True, verbose_name='Номер дома')
    products = models.ManyToManyField('Product', verbose_name='Продукты', related_name='seller')
    debt = models.DecimalField(max_digits=10, decimal_places=2, default='0.00',
                               verbose_name='Задолженность перед поставщиком')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')

    class Meta:
        verbose_name = 'Продавец'
        verbose_name_plural = 'Продавцы'

    def __str__(self):
        return self.title


class Product(models.Model):
    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    title = models.CharField(max_length=255, verbose_name='Название')
    model = models.CharField(max_length=255, verbose_name='Модель')
    released = models.DateField(verbose_name='Дата выхода продукта на рынок')

    def __str__(self):
        return f'{self.title} {self.model}, {self.released}'
