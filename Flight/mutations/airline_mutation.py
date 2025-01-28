from abc import ABC, abstractmethod
from Flight.models import Airline
import graphene
from graphene_django.types import DjangoObjectType


class AirlineCommand(ABC):
    """Base Command class for Airline operations."""
    @abstractmethod
    def execute(self, **kwargs):
        pass

    @abstractmethod
    def undo(self, **kwargs):
        pass


class CreateAirlineCommand(AirlineCommand):
    def __init__(self):
        self.airline = None  # To store the created Airline for undo

    def execute(self, airline_name, airline_code, airline_rules, airline_logo=None):
        # Check if the airline airline_code already exists
        if Airline.objects.filter(airline_code=airline_code).exists():
            raise Exception("Airline with this airline_code already exists.")
        # Create the Airline and store it for undo
        self.airline = Airline.objects.create(
            airline_name=airline_name,
            airline_code=airline_code,
            airline_rules=airline_rules,
            airline_logo=airline_logo
        )
        return self.airline

    def undo(self):
        # Delete the created Airline
        if self.airline:
            self.airline.delete()


class UpdateAirlineCommand(AirlineCommand):
    def __init__(self):
        self.previous_data = None  # To store the previous state for undo
        self.airline = None

    def execute(self, airline_code, airline_name, airline_rules, airline_logo=None):
        try:
            # Fetch the Airline and store its previous state
            self.airline = Airline.objects.get(airline_code=airline_code)
            self.previous_data = {
                "airline_name": self.airline.airline_name,
                "airline_rules": self.airline.airline_rules,
                "airline_logo": self.airline.airline_logo
            }
            # Update the Airline
            self.airline.airline_name = airline_name
            self.airline.airline_rules = airline_rules
            if airline_logo:
                self.airline.airline_logo = airline_logo
            self.airline.save()
            return self.airline
        except Airline.DoesNotExist:
            raise Exception("Airline with this airline_code does not exist.")

    def undo(self):
        # Revert the Airline to its previous state
        if self.airline and self.previous_data:
            self.airline.airline_name = self.previous_data["airline_name"]
            self.airline.airline_rules = self.previous_data["airline_rules"]
            self.airline.airline_logo = self.previous_data["airline_logo"]
            self.airline.save()


class DeleteAirlineCommand(AirlineCommand):
    def __init__(self):
        self.deleted_data = None  # To store the deleted Airline's data for undo

    def execute(self, airline_code):
        try:
            # Fetch the Airline and delete it
            airline = Airline.objects.get(airline_code=airline_code)
            self.deleted_data = {
                "airline_name": airline.airline_name,
                "airline_code": airline.airline_code,
                "airline_rules": airline.airline_rules,
                "airline_logo": airline.airline_logo
            }
            airline.delete()
            return f"Airline {airline_code} deleted successfully."
        except Airline.DoesNotExist:
            raise Exception("Airline with this airline_code does not exist.")

    def undo(self):
        # Recreate the deleted Airline
        if self.deleted_data:
            Airline.objects.create(**self.deleted_data)


class AirlineCommandHandler:
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
        command.execute()
        self.undo_stack.append(command)
        
        
# Define GraphQL Type for Airline
class AirlineType(DjangoObjectType):
    class Meta:
        model = Airline


# Shared handler instance
handler = AirlineCommandHandler()


# Define Mutation for Airline
class Mutation(graphene.ObjectType):
    create_airline = graphene.Field(
        AirlineType,
        airline_name=graphene.String(required=True),
        airline_code=graphene.String(required=True),
        airline_rules=graphene.String(required=True),
        airline_logo=graphene.String()
    )

    update_airline = graphene.Field(
        AirlineType,
        airline_code=graphene.String(required=True),
        airline_name=graphene.String(required=True),
        airline_rules=graphene.String(required=True),
        airline_logo=graphene.String()
    )

    delete_airline = graphene.String(
        airline_code=graphene.String(required=True)
    )

    undo_operation = graphene.String()
    redo_operation = graphene.String()

    def resolve_create_airline(self, info, airline_name, airline_code, airline_rules, airline_logo=None):
        # Use Command Handler to create an Airline
        command = CreateAirlineCommand()
        return handler.execute(command, airline_name=airline_name, airline_code=airline_code, airline_rules=airline_rules, airline_logo=airline_logo)

    def resolve_update_airline(self, info, airline_code, airline_name, airline_rules, airline_logo=None):
        # Use Command Handler to update an Airline
        command = UpdateAirlineCommand()
        return handler.execute(command, airline_code=airline_code, airline_name=airline_name, airline_rules=airline_rules, airline_logo=airline_logo)

    def resolve_delete_airline(self, info, airline_code):
        # Use Command Handler to delete an Airline
        command = DeleteAirlineCommand()
        return handler.execute(command, airline_code=airline_code)

    def resolve_undo_operation(self, info):
        # Undo the last operation
        handler.undo()
        return "Last operation undone successfully."

    def resolve_redo_operation(self, info):
        # Redo the last undone operation
        handler.redo()
        return "Last undone operation redone successfully."