import factory

from seller.models import Seller


class SellerFactory(factory.django.DjangoModelFactory):
    title = factory.Faker('sentence', nb_words=2)
    email = factory.Faker('email')
    country = factory.Faker('country')
    city = factory.Faker('city')
    street = factory.Faker('street_name')
    building = factory.Faker('building_number')
    debt = factory.Faker('pydecimal', left_digits=6, right_digits=2)

    class Meta:
        model = Seller
