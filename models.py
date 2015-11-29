from flask import abort
from mongoengine import *


class BaseQuerySet(QuerySet):
    """
    A base queryset with handy extras
    """

    def get_or_404(self, *args, **kwargs):
        try:
            return self.get(*args, **kwargs)
        except (MultipleObjectsReturned, DoesNotExist, ValidationError):
            abort(404)

    def first_or_404(self):

        obj = self.first()
        if obj is None:
            abort(404)

        return obj


class User(Document):
    email = StringField(required=True)
    first_name = StringField(max_length=50)
    last_name = StringField(max_length=50)
    password = StringField(max_length=200)

    meta = {'queryset_class': BaseQuerySet}


class Comment(EmbeddedDocument):
    content = StringField()
    name = StringField(max_length=120)

    def __str__(self):
        return "Comment<name:{self.name}>".format(self=self)


class Post(Document):
    title = StringField(max_length=120, required=True)
    content = StringField(max_length=520, required=True)
    author = ReferenceField(User)
    tags = ListField(StringField(max_length=30))
    comments = ListField(EmbeddedDocumentField(Comment))
    meta = {'allow_inheritance': True, 'queryset_class': BaseQuerySet}

    def __str__(self):
        return "<titile:{self.title}>".format(self=self)
