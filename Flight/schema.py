import graphene
from Flight.mutations.flight_mutation import FlightMutations
from Flight.mutations.aircraft_mutation import AircraftMutations
from Flight.mutations.airline_mutation import AirlineMutations
from Flight.mutations.airport_mutation import AirportMutations
from Flight.query import FlightQueries, AirportQueries, AirlineQueries, AircraftQueries


# Combine all mutations into a single class
class Mutation(FlightMutations, AircraftMutations, AirlineMutations, AirportMutations, graphene.ObjectType):
    pass


# Combine all queries into a single class
class Query(FlightQueries, AirportQueries, AirlineQueries, AircraftQueries, graphene.ObjectType):
    pass


# Define the schema
schema = graphene.Schema(mutation=Mutation, query=Query)