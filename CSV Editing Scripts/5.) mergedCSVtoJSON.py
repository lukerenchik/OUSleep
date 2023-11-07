import pandas as pd
import json

# Define the file path and columns to be selected
file_path = "JSON Data/BaxaMergedData.csv"
columns = ["Id", "date", "TotalSteps", "TotalDistance", "VeryActiveDistance", "ModeratelyActiveDistance", 
           "LightActiveDistance", "SedentaryActiveDistance", "VeryActiveMinutes", "FairlyActiveMinutes",
           "LightlyActiveMinutes", "SedentaryMinutes", "RestingHeartRate", "TotalMinutesAsleep", "TotalTimeInBed"]

# Read the CSV file
df = pd.read_csv(file_path, usecols=columns)

# Convert DataFrame to the desired nested dictionary structure
nested_dict = {}
for _, row in df.iterrows():
    id_val = row['Id']
    date_val = row['date']
    
    if id_val not in nested_dict:
        nested_dict[id_val] = {}
    
    # Add data under the specific 'date'
    nested_dict[id_val][date_val] = row.drop(['Id', 'date']).to_dict()

# Save the nested dictionary to JSON
output_path = "JSON Data/filtered_baxa.json"
with open(output_path, 'w') as outfile:
    json.dump(nested_dict, outfile)

print(f"Filtered data saved to {output_path}")
