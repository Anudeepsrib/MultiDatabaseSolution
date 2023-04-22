import pymongo

# Connect to the MongoDB server
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["TravelDatabase"]

# Create collections
travel_history = db.create_collection("TravelHistory")
passenger_documents = db.create_collection("PassengerDocuments")
airlines = db.create_collection("Airlines")
airports = db.create_collection("Airports")
covid_guidelines = db.create_collection("COVIDGuidelines")

print("Collections created successfully.")
