from seller.models import Seller


def provider_validator(value):
    return Seller.objects.filter(level__lte=value.level)
