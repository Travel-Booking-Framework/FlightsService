from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from .models import Aircraft, Airport, Airline, Flight


@registry.register_document
class AircraftDocument(Document):
    """
    Elasticsearch Document for Aircraft Model
    """
    class Index:
        name = 'aircrafts'  # Index name in Elasticsearch

    class Django:
        model = Aircraft  # Model being mapped to this Document

        # Fields to be indexed in Elasticsearch (using existing model fields)
        fields = [
            'aircraft_model',  # Model of the aircraft
            'aircraft_capacity',  # Capacity of the aircraft
            'aircraft_manufacturer',  # Manufacturer of the aircraft
        ]

        ignore_signals = False  # Enable signals for syncing changes
        auto_refresh = True  # Automatically refresh the index


@registry.register_document
class AirportDocument(Document):
    """
    Elasticsearch Document for Airport Model
    """
    class Index:
        name = 'airports'  # Index name in Elasticsearch

    class Django:
        model = Airport  # Model being mapped to this Document

        # Fields to be indexed in Elasticsearch (using existing model fields)
        fields = [
            'airport_name',
            'airport_code',
            'airport_city',
            'airport_country',
        ]

        ignore_signals = False  # Enable signals for syncing changes
        auto_refresh = True  # Automatically refresh the index


@registry.register_document
class AirlineDocument(Document):
    """
    Elasticsearch Document for Airline Model
    """
    class Index:
        name = 'airlines'  # Index name in Elasticsearch

    class Django:
        model = Airline  # Model being mapped to this Document

        # Fields to be indexed in Elasticsearch (using existing model fields)
        fields = [
            'airline_name',
            'airline_code',
            'airline_rules',
        ]

        ignore_signals = False  # Enable signals for syncing changes
        auto_refresh = True  # Automatically refresh the index


@registry.register_document
class FlightDocument(Document):
    """
    Elasticsearch Document for Flight Model
    """
    class Index:
        name = 'flights'  # Index name in Elasticsearch

    class Django:
        model = Flight  # Model being mapped to this Document

        # Fields to be indexed in Elasticsearch (using existing model fields)
        fields = [
            'flight_number',
            'flight_type',
            'trip_type',
            'departure_datetime',
            'arrival_datetime',
            'cabin_type',
            'base_price',
            'final_price',
            'baggage_limit_kg',
            'flight_rules',
            'tax',
            'discount',
        ]

        # Relationships with other models (if necessary)
        related_models = ['Airport', 'Airline', 'Aircraft']

        # Enable signals to sync changes to Elasticsearch
        ignore_signals = False
        auto_refresh = True
