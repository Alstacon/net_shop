from django.contrib import admin, messages
from django.contrib.auth.models import Group
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import ngettext

from seller.models import Seller, Product


class ProductInline(admin.TabularInline):
    model = Product
    extra = 3


@admin.register(Seller)
class RetailerAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'level', 'type', 'provider_link', 'debt')
    fieldsets = [
        (None, {'fields': ('id', 'title', 'level', 'type', 'provider', 'debt', 'created')}),
        ('Contacts', {'fields': ('email',
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
    inlines = [ProductInline]
    list_filter = ('city',)
    readonly_fields = ('created', 'id', 'level')
    actions = ['clear_debt']

    def save_model(self, request, obj, form, change):
        if obj.type == Seller.SellerType.factory:
            obj.level = 0
            obj.provider = None
            Seller.objects.filter(provider=obj).update(level=1)
        if obj.provider:
            if obj.provider == obj:
                raise ValueError('Выберите другого поставщика.')
            obj.level = obj.provider.level + 1
            Seller.objects.filter(provider=obj).update(level=obj.level + 1)
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
    list_display = ('seller',
                    'title',
                    'model',
                    'released',
                    )
    readonly_fields = ('seller',)


admin.site.unregister(Group)
