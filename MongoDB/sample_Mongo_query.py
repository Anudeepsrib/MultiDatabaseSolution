import pymongo

# Connect to the MongoDB server
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["TravelDatabase"]

# Collections
travel_history = db["TravelHistory"]
passenger_documents = db["PassengerDocuments"]

# Query parameters
document_type = "Passport"

# Perform the query using the aggregation framework
pipeline = [
    {
        "$lookup": {
            "from": "PassengerDocuments",
            "localField": "PassengerID",
            "foreignField": "PassengerID",
            "as": "documents"
        }
    },
    {
        "$match": {
            "documents.DocumentType": document_type
        }
    },
    {
        "$unwind": "$documents"
    },
    {
        "$project": {
            "_id": 0,
            "PassengerID": 1,
            "Country": 1,
            "EntryDate": 1,
            "ExitDate": 1,
            "DocumentType": "$documents.DocumentType",
            "DocumentNumber": "$documents.DocumentNumber",
            "ExpirationDate": "$documents.ExpirationDate"
        }
    }
]

results = travel_history.aggregate(pipeline)

# Print the results
for result in results:
    print(result)
