
import factory
from faker import Factory

from core.models import CommentModel, PostModel, TagModel
from user_auth.models import UserModel

factory_ru = Factory.create("ru_RU")


class Tag(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: factory_ru.word())

    class Meta:
        model = TagModel


class User(factory.django.DjangoModelFactory):
    username = factory.Sequence(lambda n: "user%d" % n)
    password = factory.Sequence(lambda n: "7859375jehfwe%d" % n)
    email = factory.Sequence(lambda n: f"user{n}@example.com")

    class Meta:
        model = UserModel


class Post(factory.django.DjangoModelFactory):
    title = factory.Sequence(lambda n: factory_ru.word())
    text = factory.Sequence(lambda n: factory_ru.word())

    class Meta:
        model = PostModel


class Comment(factory.django.DjangoModelFactory):
    text = factory.Sequence(lambda n: factory_ru.word())

    class Meta:
        model = CommentModel
