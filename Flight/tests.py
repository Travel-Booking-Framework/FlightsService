from django.test import TestCase
from Flight.models import Aircraft
from Flight.mutations.aircraft_mutation import (
    CreateAircraftCommand,
    UpdateAircraftCommand,
    DeleteAircraftCommand,
    AircraftCommandHandler
)
from Flight.schema import AircraftQueries
from Flight.models import Airline
from Flight.mutations.airline_mutation import (
    CreateAirlineCommand,
    UpdateAirlineCommand,
    DeleteAirlineCommand,
    AirlineCommandHandler
)
from Flight.query import AirlineQueries
from Flight.models import Airport
from Flight.mutations.airport_mutation import (
    CreateAirportCommand,
    UpdateAirportCommand,
    DeleteAirportCommand,
    AirportCommandHandler
)
from Flight.query import AirportQueries
from Flight.models import Flight
from Flight.mutations.flight_mutation import (
    CreateFlightCommand,
    UpdateFlightCommand,
    DeleteFlightCommand,
    FlightCommandHandler
)
from Flight.query import FlightQueries


class AircraftTestCase(TestCase):
    def setUp(self):
        self.handler = AircraftCommandHandler()
        self.aircraft = Aircraft.objects.create(
            aircraft_model="Boeing 747",
            aircraft_capacity=400,
            aircraft_manufacturer="Boeing"
        )

    def test_create_aircraft(self):
        command = CreateAircraftCommand()
        created_aircraft = self.handler.execute(command,
                                                aircraft_model="Airbus A320",
                                                aircraft_capacity=180,
                                                aircraft_manufacturer="Airbus")

        self.assertEqual(Aircraft.objects.count(), 2)
        self.assertEqual(created_aircraft.aircraft_model, "Airbus A320")

    def test_create_aircraft_duplicate(self):
        command = CreateAircraftCommand()
        with self.assertRaises(Exception):
            self.handler.execute(command,
                                 aircraft_model="Boeing 747",
                                 aircraft_capacity=400,
                                 aircraft_manufacturer="Boeing")

    def test_update_aircraft(self):
        command = UpdateAircraftCommand()
        updated_aircraft = self.handler.execute(command,
                                                aircraft_model="Boeing 747",
                                                aircraft_capacity=420,
                                                aircraft_manufacturer="Boeing Updated")

        self.assertEqual(updated_aircraft.aircraft_capacity, 420)
        self.assertEqual(updated_aircraft.aircraft_manufacturer, "Boeing Updated")

    def test_update_aircraft_not_exist(self):
        command = UpdateAircraftCommand()
        with self.assertRaises(Exception):
            self.handler.execute(command,
                                 aircraft_model="Non-Existent",
                                 aircraft_capacity=250,
                                 aircraft_manufacturer="Unknown")

    def test_delete_aircraft(self):
        command = DeleteAircraftCommand()
        result = self.handler.execute(command, aircraft_model="Boeing 747")

        self.assertEqual(Aircraft.objects.count(), 0)
        self.assertEqual(result, "Aircraft Boeing 747 deleted successfully.")

    def test_delete_aircraft_not_exist(self):
        command = DeleteAircraftCommand()
        with self.assertRaises(Exception):
            self.handler.execute(command, aircraft_model="Non-Existent")

    def test_undo_create(self):
        command = CreateAircraftCommand()
        self.handler.execute(command,
                             aircraft_model="Airbus A320",
                             aircraft_capacity=180,
                             aircraft_manufacturer="Airbus")

        self.handler.undo()
        self.assertEqual(Aircraft.objects.count(), 1)

    def test_undo_update(self):
        command = UpdateAircraftCommand()
        self.handler.execute(command,
                             aircraft_model="Boeing 747",
                             aircraft_capacity=420,
                             aircraft_manufacturer="Boeing Updated")

        self.handler.undo()
        aircraft = Aircraft.objects.get(aircraft_model="Boeing 747")
        self.assertEqual(aircraft.aircraft_capacity, 400)
        self.assertEqual(aircraft.aircraft_manufacturer, "Boeing")

    def test_undo_delete(self):
        command = DeleteAircraftCommand()
        self.handler.execute(command, aircraft_model="Boeing 747")

        self.handler.undo()
        self.assertEqual(Aircraft.objects.count(), 1)

    def test_redo_create(self):
        command = CreateAircraftCommand()
        created_aircraft = self.handler.execute(command,
                                                aircraft_model="Airbus A320",
                                                aircraft_capacity=180,
                                                aircraft_manufacturer="Airbus"
                                                )

        self.handler.undo()
        self.handler.redo()

        self.assertEqual(Aircraft.objects.count(), 2)

    def test_query_all_aircrafts(self):
        query = AircraftQueries()
        result = query.resolve_all_aircrafts(None)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].aircraft_model, "Boeing 747")

    def test_query_aircraft_by_model(self):
        query = AircraftQueries()
        result = query.resolve_aircraft_by_model(None, aircraft_model="Boeing 747")

        self.assertIsNotNone(result)
        self.assertEqual(result.aircraft_model, "Boeing 747")

    def test_query_aircraft_by_model_not_exist(self):
        query = AircraftQueries()
        result = query.resolve_aircraft_by_model(None, aircraft_model="Non-Existent")

        self.assertIsNone(result)


class AirlineTestCase(TestCase):
    def setUp(self):
        self.handler = AirlineCommandHandler()
        self.airline = Airline.objects.create(
            airline_name="Emirates",
            airline_code="EK",
            airline_rules="Standard international rules",
            airline_logo=None
        )

    def test_create_airline(self):
        command = CreateAirlineCommand()
        created_airline = self.handler.execute(command,
                                               airline_name="Qatar Airways",
                                               airline_code="QR",
                                               airline_rules="Premium airline rules",
                                               airline_logo=None)

        self.assertEqual(Airline.objects.count(), 2)
        self.assertEqual(created_airline.airline_name, "Qatar Airways")

    def test_create_airline_duplicate(self):
        command = CreateAirlineCommand()
        with self.assertRaises(Exception):
            self.handler.execute(command,
                                 airline_name="Duplicate Emirates",
                                 airline_code="EK",
                                 airline_rules="Should not be created",
                                 airline_logo=None)

    def test_update_airline(self):
        command = UpdateAirlineCommand()
        updated_airline = self.handler.execute(command,
                                               airline_code="EK",
                                               airline_name="Emirates Updated",
                                               airline_rules="Updated rules",
                                               airline_logo=None)

        self.assertEqual(updated_airline.airline_name, "Emirates Updated")

    def test_update_airline_not_exist(self):
        command = UpdateAirlineCommand()
        with self.assertRaises(Exception):
            self.handler.execute(command,
                                 airline_code="NONEXISTENT",
                                 airline_name="Fake Airline",
                                 airline_rules="No rules",
                                 airline_logo=None)

    def test_delete_airline(self):
        command = DeleteAirlineCommand()
        result = self.handler.execute(command, airline_code="EK")

        self.assertEqual(Airline.objects.count(), 0)
        self.assertEqual(result, "Airline EK deleted successfully.")

    def test_delete_airline_not_exist(self):
        command = DeleteAirlineCommand()
        with self.assertRaises(Exception):
            self.handler.execute(command, airline_code="NONEXISTENT")

    def test_undo_create(self):
        command = CreateAirlineCommand()
        self.handler.execute(command,
                             airline_name="Qatar Airways",
                             airline_code="QR",
                             airline_rules="Premium airline rules",
                             airline_logo=None)

        self.handler.undo()
        self.assertEqual(Airline.objects.count(), 1)

    def test_undo_update(self):
        command = UpdateAirlineCommand()
        self.handler.execute(command,
                             airline_code="EK",
                             airline_name="Emirates Updated",
                             airline_rules="Updated rules",
                             airline_logo=None)

        self.handler.undo()
        airline = Airline.objects.get(airline_code="EK")
        self.assertEqual(airline.airline_name, "Emirates")

    def test_undo_delete(self):
        command = DeleteAirlineCommand()
        self.handler.execute(command, airline_code="EK")

        self.handler.undo()
        self.assertEqual(Airline.objects.count(), 1)

    def test_redo_create(self):
        command = CreateAirlineCommand()
        self.handler.execute(command,
                             airline_name="Qatar Airways",
                             airline_code="QR",
                             airline_rules="Premium airline rules",
                             airline_logo=None)

        self.handler.undo()
        self.handler.redo()
        self.assertEqual(Airline.objects.count(), 2)

    def test_query_all_airlines(self):
        query = AirlineQueries()
        result = query.resolve_all_airlines(None)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].airline_code, "EK")

    def test_query_airline_by_code(self):
        query = AirlineQueries()
        result = query.resolve_airline_by_code(None, airline_code="EK")

        self.assertIsNotNone(result)
        self.assertEqual(result.airline_code, "EK")

    def test_query_airline_by_code_not_exist(self):
        query = AirlineQueries()
        result = query.resolve_airline_by_code(None, airline_code="NONEXISTENT")

        self.assertIsNone(result)


class AirportTestCase(TestCase):
    def setUp(self):
        self.handler = AirportCommandHandler()
        self.airport = Airport.objects.create(
            airport_code="DXB",
            airport_name="Dubai International Airport",
            airport_city="Dubai",
            airport_country="UAE"
        )

    def test_create_airport(self):
        command = CreateAirportCommand()
        created_airport = self.handler.execute(command,
                                               airport_code="JFK",
                                               airport_name="John F. Kennedy International Airport",
                                               airport_city="New York",
                                               airport_country="USA")

        self.assertEqual(Airport.objects.count(), 2)
        self.assertEqual(created_airport.airport_code, "JFK")

    def test_update_airport(self):
        command = UpdateAirportCommand()
        updated_airport = self.handler.execute(command,
                                               airport_code="DXB",
                                               airport_name="Dubai Updated",
                                               airport_city="Dubai",
                                               airport_country="UAE")

        self.assertEqual(updated_airport.airport_name, "Dubai Updated")

    def test_delete_airport(self):
        command = DeleteAirportCommand()
        result = self.handler.execute(command, airport_code="DXB")

        self.assertEqual(Airport.objects.count(), 0)
        self.assertEqual(result, "Airport DXB deleted successfully.")

    def test_undo_create(self):
        command = CreateAirportCommand()
        self.handler.execute(command,
                             airport_code="JFK",
                             airport_name="John F. Kennedy International Airport",
                             airport_city="New York",
                             airport_country="USA")

        self.handler.undo()
        self.assertEqual(Airport.objects.count(), 1)

    def test_undo_update(self):
        command = UpdateAirportCommand()
        self.handler.execute(command,
                             airport_code="DXB",
                             airport_name="Dubai Updated",
                             airport_city="Dubai",
                             airport_country="UAE")

        self.handler.undo()
        airport = Airport.objects.get(airport_code="DXB")
        self.assertEqual(airport.airport_name, "Dubai International Airport")

    def test_undo_delete(self):
        command = DeleteAirportCommand()
        self.handler.execute(command, airport_code="DXB")

        self.handler.undo()
        self.assertEqual(Airport.objects.count(), 1)

    def test_redo_create(self):
        command = CreateAirportCommand()
        self.handler.execute(command,
                             airport_code="JFK",
                             airport_name="John F. Kennedy International Airport",
                             airport_city="New York",
                             airport_country="USA")

        self.handler.undo()
        self.handler.redo()
        self.assertEqual(Airport.objects.count(), 2)

    def test_query_all_airports(self):
        query = AirportQueries()
        result = query.resolve_all_airports(None)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].airport_code, "DXB")

    def test_query_airport_by_code(self):
        query = AirportQueries()
        result = query.resolve_airport_by_code(None, airport_code="DXB")

        self.assertIsNotNone(result)
        self.assertEqual(result.airport_code, "DXB")

    def test_redo_create(self):
        command = CreateAirportCommand()
        created_airport = self.handler.execute(command,
                                               airport_code="LAX",
                                               airport_name="Los Angeles International Airport",
                                               airport_city="Los Angeles",
                                               airport_country="USA")

        self.handler.undo()

        self.handler.redo()

        self.assertEqual(Airport.objects.count(), 2)
        self.assertEqual(Airport.objects.get(airport_code="LAX").airport_name, "Los Angeles International Airport")


class FlightTestCase(TestCase):
    def setUp(self):
        self.handler = FlightCommandHandler()

        # ایجاد نمونه‌های مورد نیاز
        self.departure_airport = Airport.objects.create(
            airport_code="DXB",
            airport_name="Dubai International Airport",
            airport_city="Dubai",
            airport_country="UAE"
        )

        self.arrival_airport = Airport.objects.create(
            airport_code="JFK",
            airport_name="John F. Kennedy International Airport",
            airport_city="New York",
            airport_country="USA"
        )

        self.airline = Airline.objects.create(
            airline_code="EK",
            airline_name="Emirates",
            airline_rules="Rulesss..."
        )

        self.aircraft = Aircraft.objects.create(
            aircraft_model="Boeing 777",
            aircraft_capacity=396,
            aircraft_manufacturer="Boeing"
        )

        # ایجاد یک نمونه از Flight
        self.flight = Flight.objects.create(
            flight_number="EK202",
            flight_type="International",
            trip_type="One-Way",
            departure_airport=self.departure_airport,
            arrival_airport=self.arrival_airport,
            departure_datetime="2025-02-02T10:00:00Z",
            arrival_datetime="2025-02-02T14:00:00Z",
            airline=self.airline,  # مقدار درست شده
            aircraft=self.aircraft,  # مقدار درست شده
            cabin_type="Economy",
            base_price=500,
            tax=50,
            discount=10.0,
            baggage_limit_kg=30.0,
            flight_rules="Standard rules"
        )

    def test_create_flight(self):
        command = CreateFlightCommand()
        created_flight = self.handler.execute(command,
                                              flight_number="QR101",
                                              flight_type="Domestic",
                                              trip_type="Round-Trip",
                                              departure_airport=self.departure_airport,  # مقدار درست شده
                                              arrival_airport=self.arrival_airport,  # مقدار درست شده
                                              departure_datetime="2025-03-01T12:00:00Z",
                                              arrival_datetime="2025-03-01T16:00:00Z",
                                              airline=self.airline,  # مقدار درست شده
                                              aircraft=self.aircraft,  # مقدار درست شده
                                              cabin_type="Business",
                                              base_price=800,
                                              tax=80,
                                              discount=15.0,
                                              baggage_limit_kg=40.0,
                                              flight_rules="Business class rules")

        self.assertEqual(Flight.objects.count(), 2)
        self.assertEqual(created_flight.flight_number, "QR101")

    def test_update_flight(self):
        command = UpdateFlightCommand()
        updated_flight = self.handler.execute(command,
            flight_number="EK202",
            base_price=600,
            baggage_limit_kg=35.0)

        self.assertEqual(updated_flight.base_price, 600)
        self.assertEqual(updated_flight.baggage_limit_kg, 35.0)

    def test_delete_flight(self):
        command = DeleteFlightCommand()
        result = self.handler.execute(command, flight_number="EK202")

        self.assertEqual(Flight.objects.count(), 0)
        self.assertEqual(result, "Flight EK202 deleted successfully.")

    def test_undo_create(self):
        command = CreateFlightCommand()
        self.handler.execute(command,
                             flight_number="QR102",
                             flight_type="International",
                             trip_type="One-Way",
                             departure_airport=self.departure_airport,  # مقدار درست شده
                             arrival_airport=self.arrival_airport,  # مقدار درست شده
                             departure_datetime="2025-04-01T10:00:00Z",
                             arrival_datetime="2025-04-01T14:00:00Z",
                             airline=self.airline,  # مقدار درست شده
                             aircraft=self.aircraft,  # مقدار درست شده
                             cabin_type="First Class",
                             base_price=1500,
                             tax=200,
                             discount=20.0,
                             baggage_limit_kg=50.0,
                             flight_rules="Luxury travel")

        self.handler.undo()
        self.assertEqual(Flight.objects.count(), 1)

    def test_undo_delete(self):
        command = DeleteFlightCommand()
        self.handler.execute(command, flight_number="EK202")

        self.handler.undo()
        self.assertEqual(Flight.objects.count(), 1)

    def test_redo_create(self):
        command = CreateFlightCommand()
        created_flight = self.handler.execute(command,
                                              flight_number="QR200",
                                              flight_type="Domestic",
                                              trip_type="Round-Trip",
                                              departure_airport=self.departure_airport,  # مقدار درست شده
                                              arrival_airport=self.arrival_airport,  # مقدار درست شده
                                              departure_datetime="2025-05-01T12:00:00Z",
                                              arrival_datetime="2025-05-01T16:00:00Z",
                                              airline=self.airline,  # مقدار درست شده
                                              aircraft=self.aircraft,  # مقدار درست شده
                                              cabin_type="Economy",
                                              base_price=400,
                                              tax=40,
                                              discount=5.0,
                                              baggage_limit_kg=20.0,
                                              flight_rules="Basic economy rules")

        self.handler.undo()
        self.handler.redo()

        self.assertEqual(Flight.objects.count(), 2)
        self.assertEqual(Flight.objects.get(flight_number="QR200").base_price, 400)

    def test_query_all_flights(self):
        query = FlightQueries()
        result = query.resolve_all_flights(None)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].flight_number, "EK202")

    def test_query_flight_by_number(self):
        query = FlightQueries()
        result = query.resolve_flight_by_number(None, flight_number="EK202")

        self.assertIsNotNone(result)
        self.assertEqual(result.flight_number, "EK202")

    def test_query_flight_by_number_not_exist(self):
        query = FlightQueries()
        result = query.resolve_flight_by_number(None, flight_number="INVALID123")

        self.assertIsNone(result)