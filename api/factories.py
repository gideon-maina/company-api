from django.contrib.auth.models import User
from factory import DjangoModelFactory, Faker

from .models import Company


class UserFactory(DjangoModelFactory):
    username = Faker('name')
    email = Faker('email')

    class Meta:
        model = User


class CompanyFactory(DjangoModelFactory):
    name = Faker('company')
    description = Faker('text')
    website = Faker('url')
    street_line_1 = Faker('street_address')
    city = Faker('city')
    state = Faker('state_abbr')
    zipcode = Faker('zipcode')

    class Meta:
        model = Company
