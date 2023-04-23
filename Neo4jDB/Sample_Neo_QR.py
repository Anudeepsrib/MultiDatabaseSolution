from py2neo import Graph

# Connect to the Neo4j Aura database
neo4j_url = "neo4j+s://0a1b6132.databases.neo4j.io:7687"
neo4j_user = "neo4j"
neo4j_password = "tblsM1McIuoKpLePTKRWyMOyysg0j4asgxlC3odhOuA"
graph = Graph(neo4j_url, auth=(neo4j_user, neo4j_password))

# Define query parameters
country_name = "USA"
airline_name = "Delta Air Lines"

# Define Cypher query to find all passengers who traveled from a specific country and took a flight operated by a specific airline
cypher_query = f"""
    MATCH (p:Passenger)-[:TOOK_FLIGHT]->(f:Flight)<-[:FLIES_FOR]-(a:Airline {{Name: "{airline_name}"}})
    WHERE (f)-[:DEPARTS_FROM]->()<-[:SUBJECT_TO_GUIDELINES]-(:Country {{Name: "{country_name}"}})
    RETURN p.FirstName, p.LastName, f.DepartureAirport, f.ArrivalAirport, f.DepartureTime
"""

# Execute Cypher query and get results
results = graph.run(cypher_query)

# Print results
for record in results:
    print(record["p.FirstName"], record["p.LastName"], record["f.DepartureAirport"], record["f.ArrivalAirport"], record["f.DepartureTime"])
