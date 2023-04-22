import boto3
import random
from faker import Faker
from datetime import datetime, timedelta

# Create a DynamoDB client
dynamodb = boto3.resource('dynamodb')
fake = Faker()

# Table references
flight_schedules_table = dynamodb.Table('FlightSchedules')
flight_airports_table = dynamodb.Table('FlightAirports')
flight_airlines_table = dynamodb.Table('FlightAirlines')
flight_passengers_table = dynamodb.Table('FlightPassengers')
flight_covid_guidelines_table = dynamodb.Table('FlightCovidGuidelines')

# Functions to insert random data
def insert_flight_schedules(records_count, airline_iata_codes):
    for _ in range(records_count):
        flight_number = f"{fake.random_letter().upper()}{fake.random_letter().upper()}{fake.random_number(4)}"
        departure_date = fake.date_between(start_date='-30d', end_date='+30d').strftime("%Y-%m-%d")

        flight_schedules_table.put_item(
            Item={
                'FlightNumber': flight_number,
                'DepartureDate': departure_date,
                'ArrivalDate': (datetime.strptime(departure_date, "%Y-%m-%d") + timedelta(hours=2)).strftime("%Y-%m-%d"),
                'Airline': random.choice(airline_iata_codes)
            }
        )


def insert_flight_airports(records_count):
    for _ in range(records_count):
        flight_airports_table.put_item(
            Item={
                'IATA': f"{fake.random_letter().upper()}{fake.random_letter().upper()}{fake.random_letter().upper()}",
                'Name': fake.company(),
                'City': fake.city(),
                'Country': fake.country()
            }
        )


def insert_flight_airlines(records_count):
    iata_codes = []
    for _ in range(records_count):
        iata = f"{fake.random_letter().upper()}{fake.random_letter().upper()}"
        flight_airlines_table.put_item(
            Item={
                'IATA': iata,
                'Name': fake.company(),
                'Headquarters': fake.address()
            }
        )
        iata_codes.append(iata)
    return iata_codes


def insert_flight_passengers(records_count):
    for _ in range(records_count):
        flight_passengers_table.put_item(
            Item={
                'PassengerID': f"P{fake.random_number(6)}",
                'Name': fake.name(),
                'Birthdate': fake.date_of_birth(minimum_age=10, maximum_age=90).strftime("%Y-%m-%d")
            }
        )


def insert_flight_covid_guidelines(records_count):
    for _ in range(records_count):
        flight_covid_guidelines_table.put_item(
            Item={
                'Country': fake.country(),
                'MaskMandate': random.choice([True, False]),
                'SocialDistancing': random.choice([True, False]),
                'QuarantineRequirements': random.choice([True, False])
            }
        )


def main():
    record_count = 50

    airline_iata_codes = insert_flight_airlines(record_count)
    insert_flight_schedules(record_count, airline_iata_codes)
    insert_flight_airports(record_count)
    insert_flight_passengers(record_count)
    insert_flight_covid_guidelines(record_count)

    print(f"Inserted {record_count} random records in each DynamoDB table.")


if __name__ == '__main__':
    main()
