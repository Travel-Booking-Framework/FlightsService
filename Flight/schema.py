import graphene
from Flight.mutations.flight_mutation import FlightMutations
from Flight.mutations.aircraft_mutation import AircraftMutations
from Flight.mutations.airline_mutation import AirlineMutations
from Flight.mutations.airport_mutation import AirportMutations


# Combine all mutations into a single class
class Mutation(FlightMutations, AircraftMutations, AirlineMutations, AirportMutations, graphene.ObjectType):
    pass


# Define the schema
schema = graphene.Schema(mutation=Mutation)