from seller.models import Seller


def update_level_obj(obj: Seller):
    Seller.objects.filter(provider=obj).update(level=obj.level + 1)
    buyers = Seller.objects.filter(provider=obj)
    for obj in buyers:
        update_level_obj(obj)


def update_level_instance(obj: Seller):
    Seller.objects.filter(provider=obj).update(level=obj.level + 1)
    obj.save()
    buyers = Seller.objects.filter(provider=obj)
    for obj in buyers:
        update_level_instance(obj)
