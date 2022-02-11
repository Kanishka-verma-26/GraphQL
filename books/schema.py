import graphene
from graphene_django import DjangoObjectType
from .models import Books


# as we are taking our data and we're basically formatting that into a type that can be utilize here and
# GraphQL presents your database objects as a graph structure i.e. modelling your databse using traditional methods
#  DjangoObjectType will present all fields on a Model through GraphQL, its automatically gonna define grapgql fields here so this will get formatted into graphql fields and then corresponds to the fields on the django model
# we want to know some information about those fields so that we can convert this, so that GraphQL can essentially make a graph from the data ; so that we can generate queries for our data


class BooksType(DjangoObjectType):
    class Meta:
        model = Books           # model that we want to use
        fields = ("id","title","excerpt")       # data that we want to collect

# the above data might be translated something like below:

# type Books {
#     id: id
#     'title': String
#     Excerpt: String
# }


# now we need a way of kind of generating a query so that we can actually kind of run a query
# behind the scene we want to convert out data into something like this for graphql utilizing :

# type Query {
#     me: User
# }

# the our data can be translated into something like:

class Query(graphene.ObjectType):               # you can use the standard "ObjectType" to create custom fields or to provide an abstraction between your internal Django models and your external API.

    all_books = graphene.List(BooksType)

    def resolve_all_books(root,info):
        # return Books.objects.all()
        return Books.objects.exclude(title="django")


schema = graphene.Schema(query=Query)


