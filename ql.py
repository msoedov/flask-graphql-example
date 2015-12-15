import logging
from functools import lru_cache

import graphene
import trafaret as t

from models import Post, User, Comment


logger = logging.getLogger(__package__)


@lru_cache()
def get_comments_by_id(post_id):
    return Post.objects.get(id=post_id).comments


def construct(object_type, mongo_obj):
    field_names = [f.attname for f in object_type._meta.fields]
    if 'id' in field_names:
        field_names.append('_id')
    kwargs = {attr: val for attr, val in mongo_obj.to_mongo().items()
              if attr in field_names}
    if '_id' in kwargs:
        kwargs['id'] = kwargs.pop('_id')
    return object_type(**kwargs)


class CommentField(graphene.ObjectType):
    content = graphene.String()
    name = graphene.String()


class PostField(graphene.ObjectType):
    id = graphene.String()
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
    id = graphene.String()
    email = graphene.String()
    last_name = graphene.String()
    posts = graphene.List(PostField)

    @graphene.resolve_only_args
    def resolve_posts(self):
        posts = Post.objects.filter(author=self.id)
        return [construct(PostField, p) for p in posts]


class UserMutation(graphene.Mutation):

    class Input(object):
        """Params for User class"""
        first_name = graphene.String()
        last_name = graphene.String()
        email = graphene.String()

    user = graphene.Field(UserField)

    @classmethod
    def mutate(cls, _, info, __):
        logger.debug("agrs %s", info)
        user_schema = t.Dict({
            'email': t.String(min_length=2),
            'first_name': t.String(min_length=2),
            'last_name': t.String(min_length=2),
        })

        user_data = user_schema.check(info)
        user = User.objects.create(**user_data)
        user.save()
        return cls(user=construct(UserField, user))


class PostMutation(graphene.Mutation):

    class Input(object):
        """Params for Post class"""
        user_id = graphene.String()
        title = graphene.String()
        content = graphene.String()
        tags = graphene.List(graphene.String)

    post = graphene.Field(PostField)

    @classmethod
    def mutate(cls, _, info, __):
        logger.debug("agrs %s", info)
        post_schema = t.Dict({
            'title': t.String(min_length=2),
            'user_id': t.String(min_length=2),
            'content': t.String(min_length=2),
            t.Key('tags',
                  optional=True): t.List(t.String,
                                         min_length=1),
        })

        post_data = post_schema.check(info)
        user_id = post_data.pop('user_id')
        user = User.objects.get_or_404(id=user_id)
        post = Post(author=user, **post_data)
        post.save()
        return cls(post=construct(PostField, post))


class CommentMutation(graphene.Mutation):

    class Input(object):
        """Params for Comment class"""
        post_id = graphene.String()
        content = graphene.String()
        name = graphene.String()

    comment = graphene.Field(CommentField)
    post = graphene.Field(PostField)

    @classmethod
    def mutate(cls, _, info, __):
        logger.debug("agrs %s", info)
        comment_schema = t.Dict({
            'name': t.String(min_length=2, max_length=30),
            'post_id': t.String(min_length=2, max_length=30),
            'content': t.String(min_length=2), })

        comment_data = comment_schema.check(info)
        post_id = comment_data.pop('post_id')
        post = Post.objects.get_or_404(id=post_id)
        comment = Comment(**comment_data)
        post.comments.append(comment)
        post.save()
        return cls(post=construct(PostField, post), comment=construct(CommentField, comment))


class UserQuery(graphene.ObjectType):
    user = graphene.Field(UserField, email=graphene.Argument(graphene.String))
    ping = graphene.String(description='Ping someone',
                           to=graphene.Argument(graphene.String))

    def resolve_user(self, args, info):
        u = User.objects.get(email=args.get('email'))
        return construct(UserField, u)

    def resolve_ping(self, args, info):
        return 'Pinging {}'.format(args.get('to'))


class UserMutationQuery(graphene.ObjectType):
    create_user = graphene.Field(UserMutation)
    create_post = graphene.Field(PostMutation)
    make_comment = graphene.Field(CommentMutation)

schema = graphene.Schema(query=UserQuery, mutation=UserMutationQuery)
