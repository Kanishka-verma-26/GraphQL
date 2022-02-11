from django.urls import path
from graphene_django.views import GraphQLView

# yoy can define the schema like below in the urls.py file or you can define it into your settings.py file like
# GRAPHENE = {
#     'SCHEMA': 'quiz.schema.schema'  #  change your path
# }
from quiz.schema import schema


urlpatterns = [
    path("graphql",GraphQLView.as_view(graphiql=True, schema=schema)),
]