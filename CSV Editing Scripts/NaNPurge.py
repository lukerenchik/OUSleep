import json
import math

# Load the JSON data
input_path = "/Users/user/PycharmProjects/OUSleep/filtered_baxa.json"
with open(input_path, 'r') as infile:
    data = json.load(infile)

# Check for NaN in the nested dictionaries and remove them
for user_id in list(data.keys()):  # Using list to avoid runtime error due to changing size during iteration
    for date in list(data[user_id].keys()):
        if any(isinstance(val, float) and math.isnan(val) for val in data[user_id][date].values()):
            del data[user_id][date]
    # If after removal, a user_id has no date entries, remove user_id
    if not data[user_id]:
        del data[user_id]

# Save the cleaned data back to the JSON file
with open(input_path, 'w') as outfile:
    json.dump(data, outfile)

print(f"NaN values removed and data saved to {input_path}")
