import random
from datetime import date, datetime, timedelta
from faker import Faker
import pymongo

fake = Faker()

# Connect to the MongoDB server
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["TravelDatabase"]

# Collections
travel_history = db["TravelHistory"]
passenger_documents = db["PassengerDocuments"]
airlines = db["Airlines"]
airports = db["Airports"]
covid_guidelines = db["COVIDGuidelines"]

# Generate random data
num_records = 100
document_types = ['Passport', 'ID Card', 'Visa']
mask_mandate_statuses = [True, False]
social_distancing_statuses = [True, False]
travel_restrictions = ['None', 'Partial', 'Full']

travel_history_data = []
passenger_documents_data = []
airlines_data = []
airports_data = []
covid_guidelines_data = []

for _ in range(num_records):
    # TravelHistory
    travel_history_record = {
        "PassengerID": fake.uuid4(),
        "Country": fake.country(),
        "EntryDate": datetime.combine(fake.date_between(start_date='-1y', end_date='today'), datetime.min.time()),
        "ExitDate": datetime.combine(fake.date_between(start_date='today', end_date='+1y'), datetime.min.time())
    }
    travel_history_data.append(travel_history_record)

    # PassengerDocuments
    passenger_document_record = {
        "PassengerID": travel_history_record["PassengerID"],
        "DocumentType": random.choice(document_types),
        "DocumentNumber": fake.bothify(text='??######'),
        "ExpirationDate": datetime.combine(fake.date_between(start_date='today', end_date='+10y'), datetime.min.time())
    }
    passenger_documents_data.append(passenger_document_record)

    # Airlines
    airline_record = {
        "Name": fake.company(),
        "IATA": fake.bothify(text='??'),
        "ICAO": fake.bothify(text='???'),
        "Headquarters": fake.city()
    }
    airlines_data.append(airline_record)

    # Airports
    airport_record = {
        "Name": f"{fake.city()} International Airport",
        "IATA": fake.bothify(text='??'),
        "ICAO": fake.bothify(text='???'),
        "Country": fake.country(),
        "City": fake.city()
    }
    airports_data.append(airport_record)

    # COVIDGuidelines
    covid_guidelines_record = {
        "Country": airport_record["Country"],
        "MaskMandate": random.choice(mask_mandate_statuses),
        "SocialDistancing": random.choice(social_distancing_statuses),
        "QuarantineRequirements": f"{random.randint(0, 14)} days",
        "TravelRestrictions": random.choice(travel_restrictions)
    }
    covid_guidelines_data.append(covid_guidelines_record)

# Insert bulk data
travel_history.insert_many(travel_history_data)
passenger_documents.insert_many(passenger_documents_data)
airlines.insert_many(airlines_data)
airports.insert_many(airports_data)
covid_guidelines.insert_many(covid_guidelines_data)

print("Random data inserted successfully.")