from abc import ABC, abstractmethod
from Flight.models import Flight
import graphene
from graphene_django.types import DjangoObjectType


class FlightCommand(ABC):
    """Base Command class for Flight operations."""
    @abstractmethod
    def execute(self, **kwargs):
        pass

    @abstractmethod
    def undo(self, **kwargs):
        pass


class CreateFlightCommand(FlightCommand):
    def __init__(self):
        self.flight = None  # To store the created Flight for undo

    def execute(self, flight_number, flight_type, trip_type, departure_airport, arrival_airport,
                departure_datetime, arrival_datetime, airline, aircraft, cabin_type,
                base_price, tax, discount, baggage_limit_kg, flight_rules):
        # Check if the flight number already exists
        if Flight.objects.filter(flight_number=flight_number).exists():
            raise Exception("Flight with this number already exists.")
        # Create the Flight and store it for undo
        self.flight = Flight.objects.create(
            flight_number=flight_number,
            flight_type=flight_type,
            trip_type=trip_type,
            departure_airport=departure_airport,
            arrival_airport=arrival_airport,
            departure_datetime=departure_datetime,
            arrival_datetime=arrival_datetime,
            airline=airline,
            aircraft=aircraft,
            cabin_type=cabin_type,
            base_price=base_price,
            tax=tax,
            discount=discount,
            baggage_limit_kg=baggage_limit_kg,
            flight_rules=flight_rules
        )
        return self.flight

    def undo(self):
        # Delete the created Flight
        if self.flight:
            self.flight.delete()


class UpdateFlightCommand(FlightCommand):
    def __init__(self):
        self.previous_data = None  # To store the previous state for undo
        self.flight = None

    def execute(self, flight_number, **kwargs):
        try:
            # Fetch the Flight and store its previous state
            self.flight = Flight.objects.get(flight_number=flight_number)
            self.previous_data = {
                field: getattr(self.flight, field) for field in kwargs
            }
            # Update the Flight
            for field, value in kwargs.items():
                setattr(self.flight, field, value)
            self.flight.save()
            return self.flight
        except Flight.DoesNotExist:
            raise Exception("Flight with this number does not exist.")

    def undo(self):
        # Revert the Flight to its previous state
        if self.flight and self.previous_data:
            for field, value in self.previous_data.items():
                setattr(self.flight, field, value)
            self.flight.save()


class DeleteFlightCommand(FlightCommand):
    def __init__(self):
        self.deleted_data = None  # To store the deleted Flight's data for undo

    def execute(self, flight_number):
        try:
            # Fetch the Flight and delete it
            flight = Flight.objects.get(flight_number=flight_number)
            self.deleted_data = {
                "flight_number": flight.flight_number,
                "flight_type": flight.flight_type,
                "trip_type": flight.trip_type,
                "departure_airport": flight.departure_airport,
                "arrival_airport": flight.arrival_airport,
                "departure_datetime": flight.departure_datetime,
                "arrival_datetime": flight.arrival_datetime,
                "airline": flight.airline,
                "aircraft": flight.aircraft,
                "cabin_type": flight.cabin_type,
                "base_price": flight.base_price,
                "tax": flight.tax,
                "discount": flight.discount,
                "baggage_limit_kg": flight.baggage_limit_kg,
                "flight_rules": flight.flight_rules
            }
            flight.delete()
            return f"Flight {flight_number} deleted successfully."
        except Flight.DoesNotExist:
            raise Exception("Flight with this number does not exist.")

    def undo(self):
        # Recreate the deleted Flight
        if self.deleted_data:
            Flight.objects.create(**self.deleted_data)


class FlightCommandHandler:
    def __init__(self):
        self.undo_stack = []  # Stack to store executed Commands
        self.redo_stack = []  # Stack to store undone Commands

    def execute(self, command, **kwargs):
        # Execute the Command and store it in the undo stack
        result = command.execute(**kwargs)
        self.undo_stack.append(command)
        self.redo_stack.clear()  # Clear redo stack since a new operation is performed
        return result

    def undo(self):
        # Undo the last operation
        if not self.undo_stack:
            raise Exception("Nothing to undo.")
        command = self.undo_stack.pop()
        command.undo()
        self.redo_stack.append(command)

    def redo(self):
        # بررسی اینکه آیا عملیاتی برای بازگردانی وجود دارد
        if not self.redo_stack:
            raise Exception("Nothing to redo.")

        command = self.redo_stack.pop()

        # اگر دستور از نوع CreateFlightCommand باشد، باید آرگومان‌های ذخیره شده را ارسال کنیم
        if isinstance(command, CreateFlightCommand):
            self.undo_stack.append(command)
            return command.execute(
                flight_number=command.flight.flight_number,
                flight_type=command.flight.flight_type,
                trip_type=command.flight.trip_type,
                departure_airport=command.flight.departure_airport,
                arrival_airport=command.flight.arrival_airport,
                departure_datetime=command.flight.departure_datetime,
                arrival_datetime=command.flight.arrival_datetime,
                airline=command.flight.airline,
                aircraft=command.flight.aircraft,
                cabin_type=command.flight.cabin_type,
                base_price=command.flight.base_price,
                tax=command.flight.tax,
                discount=command.flight.discount,
                baggage_limit_kg=command.flight.baggage_limit_kg,
                flight_rules=command.flight.flight_rules
            )

        result = command.execute()
        self.undo_stack.append(command)
        return result


# Define GraphQL Type for Flight
class FlightType(DjangoObjectType):
    class Meta:
        model = Flight


# Shared handler instance
handler = FlightCommandHandler()


# Define Mutation for Flight
class FlightMutations(graphene.ObjectType):
    create_flight = graphene.Field(
        FlightType,
        flight_number=graphene.String(required=True),
        flight_type=graphene.String(required=True),
        trip_type=graphene.String(required=True),
        departure_airport=graphene.Int(required=True),
        arrival_airport=graphene.Int(required=True),
        departure_datetime=graphene.String(required=True),
        arrival_datetime=graphene.String(required=True),
        airline=graphene.Int(required=True),
        aircraft=graphene.Int(required=True),
        cabin_type=graphene.String(required=True),
        base_price=graphene.Int(required=True),
        tax=graphene.Int(required=True),
        discount=graphene.Float(required=True),
        baggage_limit_kg=graphene.Float(required=True),
        flight_rules=graphene.String(required=True)
    )

    update_flight = graphene.Field(
        FlightType,
        flight_number=graphene.String(required=True),
        flight_type=graphene.String(),
        trip_type=graphene.String(),
        departure_datetime=graphene.String(),
        arrival_datetime=graphene.String(),
        base_price=graphene.Int(),
        tax=graphene.Int(),
        discount=graphene.Float(),
        baggage_limit_kg=graphene.Float(),
        flight_rules=graphene.String()
    )

    delete_flight = graphene.String(
        flight_number=graphene.String(required=True)
    )

    undo_operation = graphene.String()
    redo_operation = graphene.String()

    def resolve_create_flight(self, info, **kwargs):
        # Use Command Handler to create a Flight
        command = CreateFlightCommand()
        return handler.execute(command, **kwargs)

    def resolve_update_flight(self, info, flight_number, **kwargs):
        # Use Command Handler to update a Flight
        command = UpdateFlightCommand()
        return handler.execute(command, flight_number=flight_number, **kwargs)

    def resolve_delete_flight(self, info, flight_number):
        # Use Command Handler to delete a Flight
        command = DeleteFlightCommand()
        return handler.execute(command, flight_number=flight_number)

    def resolve_undo_operation(self, info):
        # Undo the last operation
        handler.undo()
        return "Last operation undone successfully."

    def resolve_redo_operation(self, info):
        # Redo the last undone operation
        handler.redo()
        return "Last undone operation redone successfully."