# insert_random_data.py
import random
from py2neo import Graph, Node, Relationship
from faker import Faker

# Connect to the Neo4j Aura database
neo4j_url = "neo4j+s://0a1b6132.databases.neo4j.io:7687"
neo4j_user = "neo4j"
neo4j_password = "tblsM1McIuoKpLePTKRWyMOyysg0j4asgxlC3odhOuA"

graph = Graph(neo4j_url, auth=(neo4j_user, neo4j_password))

fake = Faker()
Faker.seed(12345)  # Use a seed value for reproducible data

# Define constants
num_passengers = 100
vaccination_types = ["Pfizer", "Moderna", "AstraZeneca", "Johnson & Johnson"]
airlines = [("American Airlines", "AA", "AAL"), ("Delta Air Lines", "DL", "DAL"), ("United Airlines", "UA", "UAL")]
airports = [("JFK", "KJFK", "USA", "New York"), ("LAX", "KLAX", "USA", "Los Angeles"), ("ORD", "KORD", "USA", "Chicago")]

for _ in range(num_passengers):
    # Generate random Passenger data
    passenger_id = fake.unique.uuid4()
    first_name = fake.first_name()
    last_name = fake.last_name()
    email = fake.email()
    phone = fake.phone_number()
    vaccination_status = "Vaccinated" if random.random() < 0.8 else "Not Vaccinated"
    vaccination_type = random.choice(vaccination_types)
    negative_test_result = random.choice([True, False])
    test_date = fake.date_between(start_date="-30d", end_date="today")
    travel_history = ", ".join(fake.words(nb=random.randint(1, 5)))
    passenger_documents = ", ".join(fake.words(nb=random.randint(1, 3)))

    # Create and insert Passenger node
    passenger = Node("Passenger",
                     PassengerID=passenger_id,
                     FirstName=first_name,
                     LastName=last_name,
                     Email=email,
                     Phone=phone,
                     VaccinationStatus=vaccination_status,
                     VaccinationType=vaccination_type,
                     NegativeTestResult=negative_test_result,
                     TestDate=test_date,
                     TravelHistory=travel_history,
                     PassengerDocuments=passenger_documents)
    graph.create(passenger)

    # Randomly select airline and airports
    airline_name, airline_iata, airline_icao = random.choice(airlines)
    departure_iata, departure_icao, departure_country, departure_city = random.choice(airports)
    arrival_iata, arrival_icao, arrival_country, arrival_city = random.choice(airports)

    # Get or create the Airline and Airport nodes
    airline = graph.nodes.match("Airline", Name=airline_name).first()
    if not airline:
        airline = Node("Airline", Name=airline_name, IATA=airline_iata, ICAO=airline_icao)
        graph.create(airline)

    departure_airport = graph.nodes.match("Airport", IATA=departure_iata).first()
    if not departure_airport:
        departure_airport = Node("Airport", Name=departure_city + " Airport", IATA=departure_iata, ICAO=departure_icao, Country=departure_country, City=departure_city)
        graph.create(departure_airport)

    arrival_airport = graph.nodes.match("Airport", IATA=arrival_iata).first()
    if not arrival_airport:
        arrival_airport = Node("Airport", Name=arrival_city + " Airport", IATA=arrival_iata, ICAO=arrival_icao, Country=arrival_country, City=arrival_city)
        graph.create(arrival_airport)
# insert_random_data.py
# ...

for _ in range(num_passengers):
    # ... (previous code for generating Passenger, Airline, and Airport nodes remains the same)

    # Generate random Flight data
    flight_id = fake.unique.uuid4()
    departure_time = fake.date_time_between(start_date="-30d", end_date="+30d")
    arrival_time = fake.date_time_between(start_date=departure_time, end_date="+1d")

    # Create and insert Flight node
    flight = Node("Flight",
                  FlightID=flight_id,
                  Airline=airline_name,
                  DepartureAirport=departure_iata,
                  ArrivalAirport=arrival_iata,
                  DepartureTime=departure_time,
                  ArrivalTime=arrival_time,
                  HealthStatus="Checked",
                  Quarantine=False)
    graph.create(flight)

    # Generate random Country data if it doesn't exist
    country_node = graph.nodes.match("Country", Name=departure_country).first()
    if not country_node:
        country_node = Node("Country", Name=departure_country)
        graph.create(country_node)

    # Generate random Quarantine data
    quarantine_duration = "14 days" if random.random() < 0.5 else "None"

    # Create and insert Quarantine node
    quarantine = Node("Quarantine", PassengerID=passenger_id, Duration=quarantine_duration)
    graph.create(quarantine)

    # Generate random COVIDGuidelines data
    mask_mandate = random.choice([True, False])
    social_distancing = random.choice([True, False])
    quarantine_requirements = random.choice(["14 days", "10 days", "7 days", "None"])
    travel_restrictions = random.choice(["Negative test required", "Vaccination proof required", "None"])

    # Create and insert COVIDGuidelines node
    covid_guidelines = Node("COVIDGuidelines",
                            Country=departure_country,
                            MaskMandate=mask_mandate,
                            SocialDistancing=social_distancing,
                            QuarantineRequirements=quarantine_requirements,
                            TravelRestrictions=travel_restrictions)
    graph.create(covid_guidelines)

    # Create relationships
    graph.create(Relationship(passenger, "HAS_VACCINATION", passenger))
    graph.create(Relationship(passenger, "HAS_NEGATIVE_TEST", passenger))
    graph.create(Relationship(passenger, "TOOK_FLIGHT", flight))
    graph.create(Relationship(airline, "FLIES_FOR", flight))
    graph.create(Relationship(flight, "DEPARTS_FROM", departure_airport))
    graph.create(Relationship(flight, "ARRIVES_AT", arrival_airport))
    graph.create(Relationship(passenger, "HAS_QUARANTINE", quarantine))
    graph.create(Relationship(country_node, "SUBJECT_TO_GUIDELINES", covid_guidelines))