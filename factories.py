import factory
from faker import Factory

from models import *

fake = Factory.create()


class UserFactory(factory.mongoengine.MongoEngineFactory):

    class Meta:
        model = User

    @factory.lazy_attribute
    def email(self):
        return fake.email()

    @factory.lazy_attribute
    def first_name(self):
        return fake.first_name()

    @factory.lazy_attribute
    def last_name(self):
        return fake.last_name()


class CommentFactory(factory.mongoengine.MongoEngineFactory):

    @factory.lazy_attribute
    def name(self):
        return fake.first_name()

    @factory.lazy_attribute
    def content(self):
        return fake.text()

    class Meta:
        model = Comment


class PostFactory(factory.mongoengine.MongoEngineFactory):

    class Meta:
        model = Post

    @factory.lazy_attribute
    def title(self):
        return fake.job()

    @factory.lazy_attribute
    def author(self):
        return fake.name()

    @factory.lazy_attribute
    def tags(self):
        return [fake.user_name() for _ in range(3)]

    @factory.lazy_attribute
    def comments(self):
        return CommentFactory.create_batch(5)

    @factory.lazy_attribute
    def content(self):
        return fake.text()
