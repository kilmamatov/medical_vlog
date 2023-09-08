import datetime

import factory
from faker import Factory

from core.models import TagModel
from user_auth.models import UserModel


factory_ru = Factory.create("ru_RU")


class Tag(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: factory_ru.word())

    class Meta:
        model = TagModel
