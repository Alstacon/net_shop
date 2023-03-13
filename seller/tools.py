from seller.models import Seller


def update_level_obj(obj: Seller):
    buyers = Seller.objects.filter(provider__exact=obj.id)
    for buyer in buyers:
        buyer.level = obj.level + 1
        buyer.save()
        obj = buyer
        update_level_obj(obj)
