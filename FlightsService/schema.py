import graphene
import Flight.schema


class Query(Flight.schema.Query, graphene.ObjectType):
    pass


class Mutation(Flight.schema.Mutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)