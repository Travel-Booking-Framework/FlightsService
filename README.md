# FlightsService

## Introduction

**FlightsService** is a core microservice of the **Travel-Booking-Framework** that provides a Management system for flights, like Create - Update - Delete with **Command Pattern**.
This service is developed using **Django**, **PostgreSQL** and **Elasticsearch**. This Project has **Signals** with **Observer Pattern** for Sync PostgreSQL and Elasticsearch.

## Features

- **Flights CUD**: Add, Update and Delete Flights Models with Command Pattern.
- **Flights Simple Queries**: Filter flights by Simple Queries with Query Object Pattern.
- **Flight Signals**: Sync PostgreSQL with Elasticsearch for FlightsService microservice.

## Prerequisites

- **Python 3.x**
- **Django**
- **Elasticsearch**
- **PostgreSQL**

## Installation and Setup

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/Travel-Booking-Framework/FlightsService
   cd FlightsService
   ```

2. **Create and Activate a Virtual Environment**:

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use: venv\\Scripts\\activate
    ```

3. **Install Dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

4. **Setup PostgreSQL**: Ensure **PostgreSQL** is installed and running. Update your (`settings.py`) with the correct database credentials.

5. **Setup Elasticsearch**: Ensure that **Elasticsearch** is installed and running on your system. Update the Django settings (`settings.py`) with the correct Elasticsearch configuration.

## Project Structure

- **FlightsService/**: Contains the core settings and configurations for Django.
- **Flight/**: Manages flight-related operations and functionalities.
- **Class-Diagram/**: Provides class diagrams for understanding the project architecture.
- **logs/**: Contains logs files.

## Contribution Guidelines

We welcome contributions from the community! To contribute:

1. **Fork** the repository.
2. **Create a new branch** for your feature or bug fix.
3. **Commit** your changes.
4. **Submit a Pull Request**.


## Additional Notes

- **Create a Superuser**: To create an admin account, use the command:
  ```bash
  python manage.py createsuperuser
  ```

- **GraphQL Support**: This project includes GraphQL capabilities, which can be accessed at `/graphql/`.