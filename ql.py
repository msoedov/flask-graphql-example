from functools import lru_cache

import graphene

from models import Post, User


@lru_cache()
def get_comments_by_id(post_id):
    return Post.objects.get(id=post_id).comments


def construct(object_type, mongo_obj):
    field_names = [f.attname for f in object_type._meta.fields]
    if 'id' in field_names:
        field_names.append('_id')
    kwargs = {attr: val for attr, val in mongo_obj.to_mongo().items() if attr in field_names}
    if '_id' in kwargs:
        kwargs['id'] = kwargs.pop('_id')
    return object_type(**kwargs)


class Query(graphene.ObjectType):
    hello = graphene.String(description='A typical hello world')
    ping = graphene.String(description='Ping someone', to=graphene.Argument(graphene.String))

    def resolve_hello(self, args, info):
        return 'World'

    def resolve_ping(self, args, info):
        return 'Pinging {}'.format(args.get('to'))


class CommentField(graphene.ObjectType):
    content = graphene.String()
    name = graphene.String()


class PostField(graphene.ObjectType):
    id = graphene.Int()
    title = graphene.String()
    tags = graphene.List(graphene.String)
    etags = graphene.String()
    comments = graphene.List(CommentField)
    comments_count = graphene.Int()

    def resolve_etags(self, *a, **_):
        return "( {} )".format(self.tags)

    def resolve_comments(self, *a, **_):
        return [construct(CommentField, c) for c in get_comments_by_id(self.id)]


class UserField(graphene.ObjectType):
    id = graphene.Int()
    email = graphene.String()
    last_name = graphene.String()
    posts = graphene.List(PostField)

    @graphene.resolve_only_args
    def resolve_posts(self):
        posts = Post.objects.filter(author=self.id)
        return [construct(PostField, p) for p in posts]


class UserQuery(graphene.ObjectType):
    user = graphene.Field(UserField, email=graphene.Argument(graphene.String))
    ping = graphene.String(description='Ping someone', to=graphene.Argument(graphene.String))

    def resolve_user(self, args, info):
        u = User.objects.get(email=args.get('email'))
        return construct(UserField, u)

    def resolve_ping(self, args, info):
        return 'Pinging {}'.format(args.get('to'))


schema = graphene.Schema(query=UserQuery)
