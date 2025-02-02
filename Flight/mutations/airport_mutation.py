from abc import ABC, abstractmethod
from Flight.models import Airport
import graphene
from graphene_django.types import DjangoObjectType


class AirportCommand(ABC):
    """Base Command class for Airport operations."""
    @abstractmethod
    def execute(self, **kwargs):
        pass

    @abstractmethod
    def undo(self, **kwargs):
        pass


class CreateAirportCommand(AirportCommand):
    def __init__(self):
        self.airport = None  # To store the created Airport for undo

    def execute(self, airport_code, airport_name, airport_city, airport_country):
        # Check if the airport airport_code already exists
        if Airport.objects.filter(airport_code=airport_code).exists():
            raise Exception("Airport with this airport_code already exists.")
        # Create the Airport and store it for undo
        self.airport = Airport.objects.create(
            airport_code=airport_code,
            airport_name=airport_name,
            airport_city=airport_city,
            airport_country=airport_country
        )
        return self.airport

    def undo(self):
        # Delete the created Airport
        if self.airport:
            self.airport.delete()


class UpdateAirportCommand(AirportCommand):
    def __init__(self):
        self.previous_data = None  # To store the previous state for undo
        self.airport = None

    def execute(self, airport_code, airport_name, airport_city, airport_country):
        try:
            # Fetch the Airport and store its previous state
            self.airport = Airport.objects.get(airport_code=airport_code)
            self.previous_data = {
                "airport_name": self.airport.airport_name,
                "airport_city": self.airport.airport_city,
                "airport_country": self.airport.airport_country
            }
            # Update the Airport
            self.airport.airport_name = airport_name
            self.airport.airport_city = airport_city
            self.airport.airport_country = airport_country
            self.airport.save()
            return self.airport
        except Airport.DoesNotExist:
            raise Exception("Airport with this airport_code does not exist.")

    def undo(self):
        # Revert the Airport to its previous state
        if self.airport and self.previous_data:
            self.airport.airport_name = self.previous_data["airport_name"]
            self.airport.airport_city = self.previous_data["airport_city"]
            self.airport.airport_country = self.previous_data["airport_country"]
            self.airport.save()


class DeleteAirportCommand(AirportCommand):
    def __init__(self):
        self.deleted_data = None  # To store the deleted Airport's data for undo

    def execute(self, airport_code):
        try:
            # Fetch the Airport and delete it
            airport = Airport.objects.get(airport_code=airport_code)
            self.deleted_data = {
                "airport_code": airport.airport_code,
                "airport_name": airport.airport_name,
                "airport_city": airport.airport_city,
                "airport_country": airport.airport_country
            }
            airport.delete()
            return f"Airport {airport_code} deleted successfully."
        except Airport.DoesNotExist:
            raise Exception("Airport with this airport_code does not exist.")

    def undo(self):
        # Recreate the deleted Airport
        if self.deleted_data:
            Airport.objects.create(**self.deleted_data)


class AirportCommandHandler:
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
        # Redo the last undone operation
        if not self.redo_stack:
            raise Exception("Nothing to redo.")

        command = self.redo_stack.pop()

        # اگر دستور از نوع ایجاد باشد، باید مقادیر قبلی را پاس دهیم
        if isinstance(command, CreateAirportCommand):
            self.undo_stack.append(command)
            return command.execute(
                airport_code=command.airport.airport_code,
                airport_name=command.airport.airport_name,
                airport_city=command.airport.airport_city,
                airport_country=command.airport.airport_country
            )

        result = command.execute()
        self.undo_stack.append(command)
        return result


# Define GraphQL Type for Airport
class AirportType(DjangoObjectType):
    class Meta:
        model = Airport


# Shared handler instance
handler = AirportCommandHandler()


# Define Mutation for Airport
class AirportMutations(graphene.ObjectType):
    create_airport = graphene.Field(
        AirportType,
        airport_code=graphene.String(required=True),
        airport_name=graphene.String(required=True),
        airport_city=graphene.String(required=True),
        airport_country=graphene.String(required=True)
    )

    update_airport = graphene.Field(
        AirportType,
        airport_code=graphene.String(required=True),
        airport_name=graphene.String(required=True),
        airport_city=graphene.String(required=True),
        airport_country=graphene.String(required=True)
    )

    delete_airport = graphene.String(
        airport_code=graphene.String(required=True)
    )

    undo_operation = graphene.String()
    redo_operation = graphene.String()

    def resolve_create_airport(self, info, airport_code, airport_name, airport_city, airport_country):
        # Use Command Handler to create an Airport
        command = CreateAirportCommand()
        return handler.execute(command, airport_code=airport_code, airport_name=airport_name, airport_city=airport_city, airport_country=airport_country)

    def resolve_update_airport(self, info, airport_code, airport_name, airport_city, airport_country):
        # Use Command Handler to update an Airport
        command = UpdateAirportCommand()
        return handler.execute(command, airport_code=airport_code, airport_name=airport_name, airport_city=airport_city, airport_country=airport_country)

    def resolve_delete_airport(self, info, airport_code):
        # Use Command Handler to delete an Airport
        command = DeleteAirportCommand()
        return handler.execute(command, airport_code=airport_code)

    def resolve_undo_operation(self, info):
        # Undo the last operation
        handler.undo()
        return "Last operation undone successfully."

    def resolve_redo_operation(self, info):
        # Redo the last undone operation
        handler.redo()
        return "Last undone operation redone successfully."