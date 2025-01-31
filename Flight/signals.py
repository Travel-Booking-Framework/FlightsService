from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Airline, Airport, Aircraft, Flight
from .documents import AirlineDocument, AirportDocument, AircraftDocument, FlightDocument


# Signal for Airline model
@receiver(post_save, sender=Airline)
def update_airline_elasticsearch(sender, instance, created, **kwargs):
    if created:
        AirlineDocument().update(instance)
    else:
        AirlineDocument().update(instance)


@receiver(post_delete, sender=Airline)
def delete_airline_elasticsearch(sender, instance, **kwargs):
    AirlineDocument().delete(instance)


# Signal for Airport model
@receiver(post_save, sender=Airport)
def update_airport_elasticsearch(sender, instance, created, **kwargs):
    if created:
        AirportDocument().update(instance)
    else:
        AirportDocument().update(instance)


@receiver(post_delete, sender=Airport)
def delete_airport_elasticsearch(sender, instance, **kwargs):
    AirportDocument().delete(instance)


# Signal for Aircraft model
@receiver(post_save, sender=Aircraft)
def update_aircraft_elasticsearch(sender, instance, created, **kwargs):
    if created:
        AircraftDocument().update(instance)
    else:
        AircraftDocument().update(instance)


@receiver(post_delete, sender=Aircraft)
def delete_aircraft_elasticsearch(sender, instance, **kwargs):
    AircraftDocument().delete(instance)


@receiver(post_save, sender=Flight)
def update_elasticsearch_on_create_or_update(sender, instance, created, **kwargs):
    if created:
        # وقتی یک پرواز جدید ایجاد می‌شود، آن را در Elasticsearch ایندکس می‌کنیم
        FlightDocument().update(instance)
    else:
        # وقتی اطلاعات پرواز به‌روزرسانی می‌شود، ایندکس آن را به‌روزرسانی می‌کنیم
        FlightDocument().update(instance)


@receiver(post_delete, sender=Flight)
def delete_elasticsearch_on_delete(sender, instance, **kwargs):
    # وقتی یک پرواز حذف می‌شود، آن را از Elasticsearch حذف می‌کنیم
    FlightDocument().delete(instance)