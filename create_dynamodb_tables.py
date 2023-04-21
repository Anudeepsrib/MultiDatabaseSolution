import boto3

# Create a DynamoDB client
dynamodb = boto3.resource('dynamodb')


def create_flight_schedules_table():
    table = dynamodb.create_table(
        TableName='FlightSchedules',
        KeySchema=[
            {'AttributeName': 'FlightNumber', 'KeyType': 'HASH'},  # Partition key
            {'AttributeName': 'DepartureDate', 'KeyType': 'RANGE'}  # Sort key
        ],
        AttributeDefinitions=[
            {'AttributeName': 'FlightNumber', 'AttributeType': 'S'},
            {'AttributeName': 'DepartureDate', 'AttributeType': 'S'}
        ],
        ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
    )
    return table


def create_flight_airports_table():
    table = dynamodb.create_table(
        TableName='FlightAirports',
        KeySchema=[
            {'AttributeName': 'IATA', 'KeyType': 'HASH'}
        ],
        AttributeDefinitions=[
            {'AttributeName': 'IATA', 'AttributeType': 'S'}
        ],
        ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
    )
    return table


def create_flight_airlines_table():
    table = dynamodb.create_table(
        TableName='FlightAirlines',
        KeySchema=[
            {'AttributeName': 'IATA', 'KeyType': 'HASH'}
        ],
        AttributeDefinitions=[
            {'AttributeName': 'IATA', 'AttributeType': 'S'}
        ],
        ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
    )
    return table


def create_flight_passengers_table():
    table = dynamodb.create_table(
        TableName='FlightPassengers',
        KeySchema=[
            {'AttributeName': 'PassengerID', 'KeyType': 'HASH'}
        ],
        AttributeDefinitions=[
            {'AttributeName': 'PassengerID', 'AttributeType': 'S'}
        ],
        ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
    )
    return table


def create_flight_covid_guidelines_table():
    table = dynamodb.create_table(
        TableName='FlightCovidGuidelines',
        KeySchema=[
            {'AttributeName': 'Country', 'KeyType': 'HASH'}
        ],
        AttributeDefinitions=[
            {'AttributeName': 'Country', 'AttributeType': 'S'}
        ],
        ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
    )
    return table


def main():
    flight_schedules_table = create_flight_schedules_table()
    flight_airports_table = create_flight_airports_table()
    flight_airlines_table = create_flight_airlines_table()
    flight_passengers_table = create_flight_passengers_table()
    flight_covid_guidelines_table = create_flight_covid_guidelines_table()

    # Wait until all tables are created
    flight_schedules_table.wait_until_exists()
    flight_airports_table.wait_until_exists()
    flight_airlines_table.wait_until_exists()
    flight_passengers_table.wait_until_exists()
    flight_covid_guidelines_table.wait_until_exists()

    print("All tables created successfully!")


if __name__ == '__main__':
    main()
