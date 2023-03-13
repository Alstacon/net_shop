from django.contrib import admin, messages
from django.contrib.auth.models import Group
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import ngettext

from seller.models import Seller, Product
from seller.tools import update_level_obj


class ProductInline(admin.TabularInline):
    verbose_name = 'Продукт'
    verbose_name_plural = 'Продукты'

    model = Product.seller.through


@admin.register(Seller)
class RetailerAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'level', 'type', 'provider_link', 'debt')
    fieldsets = [
        (None, {'fields': ('id', 'title', 'level', 'type', 'provider', 'debt', 'created')}),
        ('Контакты', {'fields': ('email',
                                 'country',
                                 'city',
                                 'street',
                                 'building',)})
    ]

    def provider_link(self, obj):
        url = reverse('admin:seller_seller_change', args=(obj.provider_id,))
        if obj.provider_id:
            return format_html("<a href='{}'>{}</a>", url, obj.provider.title)
        else:
            return format_html('—')

    provider_link.admin_order_field = 'provider'
    provider_link.short_description = 'Поставщик'
    list_display_links = ('title',)
    list_filter = ('city',)
    readonly_fields = ('created', 'id', 'level', 'products')
    actions = ['clear_debt']
    inlines = [
        ProductInline,
    ]
    exclude = ('products',)

    def save_model(self, request, obj, form, change):
        if obj.type == Seller.SellerType.factory:
            obj.level = 0
            obj.provider = None
            obj.save()
            update_level_obj(obj)
        if obj.provider:
            if obj.provider == obj:
                raise ValueError('Выберите другого поставщика.')
            obj.level = obj.provider.level + 1
            obj.save()
            update_level_obj(obj)

        super().save_model(request, obj, form, change)

    @admin.action(description='Очистить задолженность перед поставщиком')
    def clear_debt(self, request, queryset):
        cleaned = queryset.update(debt=0)
        self.message_user(request, ngettext(
            '''%d Задолженность успешно очищена.''',
            '''%d Задолженности успешно очищены.''',
            cleaned,
        ) % cleaned, messages.SUCCESS)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    verbose_name = 'Продукт'
    verbose_name_plural = 'Продукты'

    list_display = ('id', 'title', 'model', 'released')
    readonly_fields = ('id',)
    list_display_links = ('title',)


admin.site.unregister(Group)
