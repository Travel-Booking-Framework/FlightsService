import graphene
from graphene_django.types import DjangoObjectType
from .models import Flight, Airport, Airline, Aircraft


# GraphQL Types for Models
class FlightType(DjangoObjectType):
    class Meta:
        model = Flight


class AirportType(DjangoObjectType):
    class Meta:
        model = Airport


class AirlineType(DjangoObjectType):
    class Meta:
        model = Airline


class AircraftType(DjangoObjectType):
    class Meta:
        model = Aircraft


# Query Classes
class FlightQueries(graphene.ObjectType):
    all_flights = graphene.List(FlightType)
    flight_by_number = graphene.Field(FlightType, flight_number=graphene.String(required=True))

    def resolve_all_flights(self, info, **kwargs):
        return Flight.objects.all()

    def resolve_flight_by_number(self, info, flight_number):
        try:
            return Flight.objects.get(flight_number=flight_number)
        except Flight.DoesNotExist:
            return None


class AirportQueries(graphene.ObjectType):
    all_airports = graphene.List(AirportType)
    airport_by_code = graphene.Field(AirportType, airport_code=graphene.String(required=True))

    def resolve_all_airports(self, info, **kwargs):
        return Airport.objects.all()

    def resolve_airport_by_code(self, info, airport_code):
        try:
            return Airport.objects.get(airport_code=airport_code)
        except Airport.DoesNotExist:
            return None


class AirlineQueries(graphene.ObjectType):
    all_airlines = graphene.List(AirlineType)
    airline_by_code = graphene.Field(AirlineType, airline_code=graphene.String(required=True))

    def resolve_all_airlines(self, info, **kwargs):
        return Airline.objects.all()

    def resolve_airline_by_code(self, info, airline_code):
        try:
            return Airline.objects.get(airline_code=airline_code)
        except Airline.DoesNotExist:
            return None


class AircraftQueries(graphene.ObjectType):
    all_aircrafts = graphene.List(AircraftType)
    aircraft_by_model = graphene.Field(AircraftType, aircraft_model=graphene.String(required=True))

    def resolve_all_aircrafts(self, info, **kwargs):
        return Aircraft.objects.all()

    def resolve_aircraft_by_model(self, info, aircraft_model):
        try:
            return Aircraft.objects.get(aircraft_model=aircraft_model)
        except Aircraft.DoesNotExist:
            return None