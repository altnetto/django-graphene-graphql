import graphene

from graphql_api import models
from graphene_django import DjangoObjectType


class UserType(DjangoObjectType):
    class Meta:
        model = models.User


class PostType(DjangoObjectType):
    class Meta:
        model = models.Post


class UserInput(graphene.InputObjectType):
    name = graphene.String()


class PostInput(graphene.InputObjectType):
    content = graphene.String()
    user_id = graphene.Int()


class CreateUser(graphene.Mutation):
    class Arguments:
        input = UserInput(required=True)

    ok = graphene.Boolean()
    user = graphene.Field(UserType)

    @staticmethod
    def mutate(root, info, input):
        instance = models.User(name=input.name)
        try:
            instance.save()
        except Exception:
            return CreateUser(ok=False, user=None)

        return CreateUser(ok=True, user=instance)


class CreatePost(graphene.Mutation):
    class Arguments:
        input = PostInput(required=True)

    ok = graphene.Boolean()
    post = graphene.Field(PostType)

    @staticmethod
    def mutate(root, info, input):
        user = models.User.objects.get(pk=input.user_id)

        if not user:
            return CreatePost(ok=False, post=None)

        instance = models.Post(content=input.content,
                               created_by=user)
        try:
            instance.save()
        except Exception:
            return CreatePost(ok=False, post=None)

        return CreatePost(ok=True, post=instance)


class Query(graphene.ObjectType):
    user = graphene.Field(UserType, id=graphene.Int())
    users = graphene.List(UserType)

    def resolve_user(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return models.User.objects.get(id=id)

        return None

    def resolve_users(self, info, **kwargs):
        return models.User.objects.all()


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    create_post = CreatePost.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
