# from django.db.models.signals import post_save, post_delete
# from django.dispatch import receiver
# from .models import Airline, Airport, Aircraft, Flight
# from .documents import AirlineDocument, AirportDocument, AircraftDocument, FlightDocument
#
#
# # Signal for Airline model
# class AirlineSignalHandler:
#     @staticmethod
#     @receiver(post_save, sender=Airline)
#     def update_airline_elasticsearch(sender, instance, created, **kwargs):
#         """
#         When an Airline is created or updated, sync it with Elasticsearch.
#         """
#         if created:
#             AirlineDocument().update(instance)
#         else:
#             AirlineDocument().update(instance)
#
#     @staticmethod
#     @receiver(post_delete, sender=Airline)
#     def delete_airline_elasticsearch(sender, instance, **kwargs):
#         """
#         When an Airline is deleted, remove it from Elasticsearch.
#         """
#         AirlineDocument().delete(instance)
#
#
# # Signal for Airport model
# class AirportSignalHandler:
#     @staticmethod
#     @receiver(post_save, sender=Airport)
#     def update_airport_elasticsearch(sender, instance, created, **kwargs):
#         """
#         When an Airport is created or updated, sync it with Elasticsearch.
#         """
#         if created:
#             AirportDocument().update(instance)
#         else:
#             AirportDocument().update(instance)
#
#     @staticmethod
#     @receiver(post_delete, sender=Airport)
#     def delete_airport_elasticsearch(sender, instance, **kwargs):
#         """
#         When an Airport is deleted, remove it from Elasticsearch.
#         """
#         AirportDocument().delete(instance)
#
#
# # Signal for Aircraft model
# class AircraftSignalHandler:
#     @staticmethod
#     @receiver(post_save, sender=Aircraft)
#     def update_aircraft_elasticsearch(sender, instance, created, **kwargs):
#         """
#         When an Aircraft is created or updated, sync it with Elasticsearch.
#         """
#         if created:
#             AircraftDocument().update(instance)
#         else:
#             AircraftDocument().update(instance)
#
#     @staticmethod
#     @receiver(post_delete, sender=Aircraft)
#     def delete_aircraft_elasticsearch(sender, instance, **kwargs):
#         """
#         When an Aircraft is deleted, remove it from Elasticsearch.
#         """
#         AircraftDocument().delete(instance)
#
#
# class FlightSignalHandler:
#     @staticmethod
#     @receiver(post_save, sender=Flight)
#     def update_flight_elasticsearch(sender, instance, created, **kwargs):
#         """
#         When a Flight is created or updated, sync it with Elasticsearch.
#         """
#         if created:
#             FlightDocument().update(instance)
#         else:
#             FlightDocument().update(instance)
#
#     @staticmethod
#     @receiver(post_delete, sender=Flight)
#     def delete_flight_elasticsearch(sender, instance, **kwargs):
#         """
#         When a Flight is deleted, remove it from Elasticsearch.
#         """
#         FlightDocument().delete(instance)