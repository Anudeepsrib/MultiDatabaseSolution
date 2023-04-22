import boto3
import pandas as pd

# Create a DynamoDB client
dynamodb = boto3.resource('dynamodb')

# Function to scan all items in a table
def scan_table(table_name):
    table = dynamodb.Table(table_name)
    response = table.scan()
    items = response['Items']

    while 'LastEvaluatedKey' in response:
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        items.extend(response['Items'])

    return items

# Scan the tables
flight_schedules = scan_table('FlightSchedules')
flight_airlines = scan_table('FlightAirlines')

# Convert to pandas dataframes
flight_schedules_df = pd.DataFrame(flight_schedules)
flight_airlines_df = pd.DataFrame(flight_airlines)

# Perform the join
result_df = pd.merge(flight_schedules_df, flight_airlines_df, left_on='Airline', right_on='IATA', how='inner')

# Save the output to a CSV file
result_df.to_csv('joined_data.csv', index=False)

print("Join completed, and output saved to joined_data.csv.")
