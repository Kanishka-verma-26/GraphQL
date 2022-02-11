import graphene
from graphene_django import DjangoObjectType
from graphene_django import DjangoListField     # "DjangoListField" allow us to generate or return lists from our databse
from .models import *

"""preparing the data so then we can put that into our query and then make a schema from it"""

class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = ("id","name")


class QuizzesType(DjangoObjectType):
    class Meta:
        model = Quizzes
        fields = ("id","title","category","quiz")


class QuestionType(DjangoObjectType):
    class Meta:
        model = Question
        fields = ("title","quiz")


class AnswerType(DjangoObjectType):
    class Meta:
        model = Answer
        fields = ("question","answer_text")


""" defining the data into the Query """

class Query(graphene.ObjectType):
    # quiz = graphene.String()

    # def resolve_quiz(root,info):            # "root" : is like an entry point into our query; "info" : allow us to pass in some information thats going to be needed to run our query
    #     return f"This is the first question"

    # going to chnge the above query into one of the models and will return data from the model refer admin file

    """returning all of the quizes"""

    """ 'DjangoListField' allows us return without the resolve function too """

    all_quizzes = DjangoListField(QuizzesType)
    all_questions = DjangoListField(QuestionType)

    def resolve_all_quizzes(root,info):
        return Quizzes.objects.all()
        # return Quizzes.objects.exclude(id=1)

    def resolve_all_questions(root,info):
        return Question.objects.all()
        # return Question.objects.exclude(id=1)


    """ inspite of 'DjangoListField' we can also use 'graphene.List' it provides a similar feature"""

    # all_quizzes = graphene.List(QuizzesType)
    # all_questions = graphene.List(QuestionType)
    #
    #
    # def resolve_all_quizzes(root, info):
    #     return Quizzes.objects.all()
    #     # return Quizzes.objects.exclude(id=1)
    #
    # def resolve_all_questions(root, info):
    #     return Question.objects.all()
    #     # return Question.objects.exclude(id=1)


    # # input example:
    # # query{
    # #  allQuizzes{
    # #   id
    # #    title
    # #  }
    # # allQuestions{
    # #    title
    # #    quiz {
    # #      id
    # #    }
    # #  }
    # #}



    """ generating arguments to have more control of what data is returned 
    (as we can set up filters in the backends such as all, filter, exclude, etc. but its not ideal 
    bcoz ideally we want to customise our query in the front end to return specific information); this method should return a single item"""

    """to return an individual item we need to change this 'graphene.List' or 'DjangoListField' to 'graphene.Field' along with the argument name """

    all_questions = graphene.Field(QuestionType, id=graphene.Int())
    all_answers = graphene.List(AnswerType, id=graphene.Int())

    def resolve_all_questions(root, info, id):
        return Question.objects.get(pk=id)

    def resolve_all_answers(root, info, id):
        return Answer.objects.filter(question=id)

    # # input example 1:
    # # query
    # # {
    # #     allQuizzes(id: 4){
    # #         title
    # #     }
    # #     allAnswers(id: 4){
    # #         answerText
    # #     }
    # # }

    # # input example 2:
    # # query
    # # GetQuestion($id: Int = 4)
    # # {
    # #     allQuestions(id:$id){
    # #     title
    # # }
    # # allAnswers(id:$id){
    # #     answerText
    # # }
    # # }


""""""'CRUD'""""""


""" adding new elements in the Category Field """

class CategoryMutationAdd(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)         # passing all the arguments present in the particular model to fetch data

    category = graphene.Field(CategoryType)         # connecting to the schema field

    @classmethod
    def mutate(cls, root,info,name):
        category = Category(name=name)
        category.save()                             # saving new category
        return CategoryMutationAdd(category=category)


""" updating existing elements in the Category Field """


class CategoryMutationUpdate(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        name = graphene.String(required=True)  # passing all the arguments present in the particular model to fetch data

    category = graphene.Field(CategoryType)  # connecting to the schema field

    @classmethod
    def mutate(cls, root, info, name, id):
        category = Category.objects.get(id=id)
        category.name = name
        category.save()  # saving new category
        return CategoryMutationUpdate(category=category)

class CategoryMutationDelete(graphene.Mutation):
    class Arguments:
        id = graphene.ID()                  # passing all the arguments present in the particular model to fetch data


    category = graphene.Field(CategoryType)  # connecting to the schema field

    @classmethod
    def mutate(cls, root, info, id):
        category = Category.objects.get(id=id)
        category.delete()  # deleting category
        return



class Mutation(graphene.ObjectType):  # Mutation allow us to create some new data in our database

    """updating and adding data to Category table"""
    update_category = CategoryMutationUpdate.Field()
    add_category = CategoryMutationAdd.Field()
    delete_category = CategoryMutationDelete.Field()



# # input example:
# mutation firstmutation
# {
#   updateCategory(id:8,name:"python"){
#     category{
#       name
#     }
#   }
#   addCategory(name:"java"){
#     category{
#       id
#       name
#     }
#   }
# }








""" building schema from the Query class """

# schema = graphene.Schema(query=Query)       # for Query class only
schema = graphene.Schema(query=Query,mutation=Mutation)        # for both query and Mutation class