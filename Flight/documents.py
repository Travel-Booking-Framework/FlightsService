from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from .models import Aircraft, Airport, Airline, Flight


@registry.register_document
class AircraftDocument(Document):
    """
    Elasticsearch Document for Aircraft Model
    """
    aircraft_model = fields.TextField()
    aircraft_capacity = fields.IntegerField()
    aircraft_manufacturer = fields.TextField()

    class Index:
        name = 'aircrafts'  # Index name in Elasticsearch

    class Django:
        model = Aircraft  # Model being mapped to this Document

        # Fields to be indexed in Elasticsearch
        fields = [
            'aircraft_model',
            'aircraft_capacity',
            'aircraft_manufacturer',
        ]

        ignore_signals = False
        auto_refresh = True


@registry.register_document
class AirportDocument(Document):
    """
    Elasticsearch Document for Airport Model
    """
    airport_name = fields.TextField()
    airport_code = fields.KeywordField()
    airport_city = fields.TextField()
    airport_country = fields.TextField()

    class Index:
        name = 'airports'  # Index name in Elasticsearch

    class Django:
        model = Airport  # Model being mapped to this Document

        # Fields to be indexed in Elasticsearch
        fields = [
            'airport_name',
            'airport_code',
            'airport_city',
            'airport_country',
        ]

        ignore_signals = False
        auto_refresh = True


@registry.register_document
class AirlineDocument(Document):
    """
    Elasticsearch Document for Airline Model
    """
    airline_name = fields.TextField()
    airline_code = fields.KeywordField()
    airline_rules = fields.TextField()
    airline_logo = fields.KeywordField()

    class Index:
        name = 'airlines'  # Index name in Elasticsearch

    class Django:
        model = Airline  # Model being mapped to this Document

        # Fields to be indexed in Elasticsearch
        fields = [
            'airline_name',
            'airline_code',
            'airline_rules',
        ]

        ignore_signals = False
        auto_refresh = True


@registry.register_document
class AirlineDocument(Document):
    class Index:
        # Index name in Elasticsearch
        name = 'airlines'

    class Django:
        model = Airline  # مدل Django که به این Document نگاشت داده می‌شود

        # فیلدهایی که باید به ایندکس اضافه شوند
        fields = [
            'airline_name',
            'airline_code',
            'airline_rules',
            'airline_logo',
        ]


@registry.register_document
class FlightDocument(Document):
    """
    Elasticsearch Document for Flight Model
    """
    # فیلدهایی که از مدل `Flight` در Elasticsearch ایندکس می‌شوند
    flight_number = fields.KeywordField()
    flight_type = fields.KeywordField()
    trip_type = fields.KeywordField()
    departure_airport = fields.ObjectField(properties={
        'name': fields.TextField(),
        'code': fields.KeywordField()
    })
    arrival_airport = fields.ObjectField(properties={
        'name': fields.TextField(),
        'code': fields.KeywordField()
    })
    departure_datetime = fields.DateField()
    arrival_datetime = fields.DateField()
    airline = fields.ObjectField(properties={
        'name': fields.TextField(),
        'code': fields.KeywordField()
    })
    aircraft = fields.ObjectField(properties={
        'model': fields.TextField(),
        'capacity': fields.IntegerField()
    })
    cabin_type = fields.KeywordField()
    base_price = fields.IntegerField()
    final_price = fields.IntegerField()
    baggage_limit_kg = fields.DecimalField()
    flight_rules = fields.TextField()

    class Index:
        # نام ایندکس در Elasticsearch
        name = 'flights'

    class Django:
        model = Flight  # مدل Django که به این Document نگاشت داده می‌شود

        # فیلدهایی که از مدل Django به Elasticsearch منتقل می‌شوند
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
        ]

        # ارتباطات با مدل‌های دیگر (در صورت لزوم)
        related_models = [ 'Airport', 'Airline', 'Aircraft' ]

        # فیلدهای متنی که باید در Elasticsearch ایندکس شوند
        ignore_signals = False  # سیگنال‌ها را فعال می‌کنیم تا همگام‌سازی در هنگام تغییرات اعمال شود
        auto_refresh = True  # ایندکس به‌صورت خودکار به‌روزرسانی می‌شود