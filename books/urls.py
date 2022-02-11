from django.urls import path
from graphene_django.views import GraphQLView


# yoy can define the schema like below in the urls.py file or you can define it into your settings.py file like
# GRAPHENE = {
#     'SCHEMA': 'books.schema.schema'  #  change your path
# }

from books.schema import schema


urlpatterns = [
    path("graphql",GraphQLView.as_view(graphiql=True, schema=schema)),   # graphiql = True give us the graphical user interface; bringing the schema that we want to use and defining the schema that we are going to use for our requests
]