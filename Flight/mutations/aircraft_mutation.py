from abc import ABC, abstractmethod
from Flight.models import Aircraft
import graphene
from graphene_django.types import DjangoObjectType


# Base Command class with abstract methods for execute and undo
class AircraftCommand(ABC):
    @abstractmethod
    def execute(self, **kwargs):
        pass

    @abstractmethod
    def undo(self, **kwargs):
        pass


# Command for creating an Aircraft
class CreateAircraftCommand(AircraftCommand):
    def __init__(self):
        self.aircraft = None  # To store the created Aircraft for undo

    def execute(self, aircraft_model, aircraft_capacity, aircraft_manufacturer):
        # Check if the aircraft_model already exists
        if Aircraft.objects.filter(aircraft_model=aircraft_model).exists():
            raise Exception("Aircraft with this aircraft_model already exists.")
        # Create the Aircraft and store it
        self.aircraft = Aircraft.objects.create(
            aircraft_model=aircraft_model,
            aircraft_capacity=aircraft_capacity,
            aircraft_manufacturer=aircraft_manufacturer
        )
        return self.aircraft

    def undo(self):
        # Delete the created Aircraft
        if self.aircraft:
            self.aircraft.delete()


# Command for updating an Aircraft
class UpdateAircraftCommand(AircraftCommand):
    def __init__(self):
        self.previous_data = None  # To store the previous state for undo
        self.aircraft = None

    def execute(self, aircraft_model, aircraft_capacity, aircraft_manufacturer):
        # Fetch the Aircraft and store its previous state
        try:
            self.aircraft = Aircraft.objects.get(aircraft_model=aircraft_model)
            self.previous_data = {
                "aircraft_capacity": self.aircraft.aircraft_capacity,
                "aircraft_manufacturer": self.aircraft.aircraft_manufacturer
            }
            # Update the Aircraft
            self.aircraft.aircraft_capacity = aircraft_capacity
            self.aircraft.aircraft_manufacturer = aircraft_manufacturer
            self.aircraft.save()
            return self.aircraft
        except Aircraft.DoesNotExist:
            raise Exception("Aircraft with this aircraft_model does not exist.")

    def undo(self):
        # Revert the Aircraft to its previous state
        if self.aircraft and self.previous_data:
            self.aircraft.aircraft_capacity = self.previous_data["aircraft_capacity"]
            self.aircraft.aircraft_manufacturer = self.previous_data["aircraft_manufacturer"]
            self.aircraft.save()


# Command for deleting an Aircraft
class DeleteAircraftCommand(AircraftCommand):
    def __init__(self):
        self.deleted_data = None  # To store the deleted Aircraft's data for undo

    def execute(self, aircraft_model):
        # Fetch the Aircraft and delete it
        try:
            aircraft = Aircraft.objects.get(aircraft_model=aircraft_model)
            self.deleted_data = {
                "aircraft_model": aircraft.aircraft_model,
                "aircraft_capacity": aircraft.aircraft_capacity,
                "aircraft_manufacturer": aircraft.aircraft_manufacturer
            }
            aircraft.delete()
            return f"Aircraft {aircraft_model} deleted successfully."
        except Aircraft.DoesNotExist:
            raise Exception("Aircraft with this aircraft_model does not exist.")

    def undo(self):
        # Recreate the deleted Aircraft
        if self.deleted_data:
            Aircraft.objects.create(**self.deleted_data)


# Handler to manage Commands and Undo/Redo
class AircraftCommandHandler:
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


# GraphQL Type for Aircraft
class AircraftType(DjangoObjectType):
    class Meta:
        aircraft_model = Aircraft


# Shared handler instance for managing Commands
handler = AircraftCommandHandler()


# GraphQL Mutations
class AircraftMutations(graphene.ObjectType):
    create_aircraft = graphene.Field(
        AircraftType,
        aircraft_model=graphene.String(required=True),
        aircraft_capacity=graphene.Int(required=True),
        aircraft_manufacturer=graphene.String(required=True)
    )

    update_aircraft = graphene.Field(
        AircraftType,
        aircraft_model=graphene.String(required=True),
        aircraft_capacity=graphene.Int(required=True),
        aircraft_manufacturer=graphene.String(required=True)
    )

    delete_aircraft = graphene.String(
        aircraft_model=graphene.String(required=True)
    )

    undo_operation = graphene.String()
    redo_operation = graphene.String()

    def resolve_create_aircraft(self, info, aircraft_model, aircraft_capacity, aircraft_manufacturer):
        # Create a new Aircraft using the Command Handler
        command = CreateAircraftCommand()
        return handler.execute(command, aircraft_model=aircraft_model, aircraft_capacity=aircraft_capacity, aircraft_manufacturer=aircraft_manufacturer)

    def resolve_update_aircraft(self, info, aircraft_model, aircraft_capacity, aircraft_manufacturer):
        # Update an Aircraft using the Command Handler
        command = UpdateAircraftCommand()
        return handler.execute(command, aircraft_model=aircraft_model, aircraft_capacity=aircraft_capacity, aircraft_manufacturer=aircraft_manufacturer)

    def resolve_delete_aircraft(self, info, aircraft_model):
        # Delete an Aircraft using the Command Handler
        command = DeleteAircraftCommand()
        return handler.execute(command, aircraft_model=aircraft_model)

    def resolve_undo_operation(self, info):
        # Undo the last operation
        handler.undo()
        return "Last operation undone successfully."

    def resolve_redo_operation(self, info):
        # Redo the last undone operation
        handler.redo()
        return "Last undone operation redone successfully."