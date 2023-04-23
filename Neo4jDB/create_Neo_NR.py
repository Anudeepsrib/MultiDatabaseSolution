# create_nodes_and_relationships.py
from py2neo import Graph, Node, Relationship

neo4j_url = "neo4j+s://0a1b6132.databases.neo4j.io:7687"
neo4j_user = "neo4j"
neo4j_password = "tblsM1McIuoKpLePTKRWyMOyysg0j4asgxlC3odhOuA"

graph = Graph(neo4j_url, auth=(neo4j_user, neo4j_password))


# Nodes
passenger = Node("Passenger",
                 PassengerID="1",
                 FirstName="John",
                 LastName="Doe",
                 Email="john.doe@example.com",
                 Phone="555-555-1234",
                 VaccinationStatus="Vaccinated",
                 VaccinationType="Pfizer",
                 NegativeTestResult=True,
                 TestDate="2021-09-15",
                 TravelHistory="USA, France, UK",
                 PassengerDocuments="Passport, Visa, Vaccination Certificate")
graph.create(passenger)

flight = Node("Flight",
              FlightID="AA100",
              Airline="American Airlines",
              DepartureAirport="JFK",
              ArrivalAirport="LAX",
              DepartureTime="2023-04-20T07:00:00",
              ArrivalTime="2023-04-20T10:00:00",
              HealthStatus="Checked",
              Quarantine=False)
graph.create(flight)

airline = Node("Airline",
               Name="American Airlines",
               IATA="AA",
               ICAO="AAL",
               Headquarters="Fort Worth, Texas, USA")
graph.create(airline)

airport_departure = Node("Airport",
                         Name="John F. Kennedy International Airport",
                         IATA="JFK",
                         ICAO="KJFK",
                         Country="USA",
                         City="New York")
graph.create(airport_departure)

airport_arrival = Node("Airport",
                       Name="Los Angeles International Airport",
                       IATA="LAX",
                       ICAO="KLAX",
                       Country="USA",
                       City="Los Angeles")
graph.create(airport_arrival)

covid_guidelines = Node("COVIDGuidelines",
                        Country="USA",
                        MaskMandate=True,
                        SocialDistancing=True,
                        QuarantineRequirements="14 days",
                        TravelRestrictions="Negative test required")
graph.create(covid_guidelines)

# Relationships
graph.create(Relationship(passenger, "HAS_VACCINATION", passenger))
graph.create(Relationship(passenger, "HAS_NEGATIVE_TEST", passenger))
graph.create(Relationship(passenger, "TOOK_FLIGHT", flight))
graph.create(Relationship(airline, "FLIES_FOR", flight))
graph.create(Relationship(flight, "DEPARTS_FROM", airport_departure))
graph.create(Relationship(flight, "ARRIVES_AT", airport_arrival))
graph.create(Relationship(passenger, "HAS_QUARANTINE", passenger))
graph.create(Relationship(covid_guidelines, "SUBJECT_TO_GUIDELINES", covid_guidelines))
