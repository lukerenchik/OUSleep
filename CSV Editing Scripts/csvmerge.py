import csv

activity_path = "/Users/user/PycharmProjects/OUSleep/Baxa_Filtered_Activity_Data.csv"
sleep_path = "/Users/user/PycharmProjects/OUSleep/BaxaSleepData_filtered.csv"
output_path = "/Users/user/PycharmProjects/OUSleep/MergedData.csv"

# Read the activity data
with open(activity_path, 'r') as act_file:
    act_reader = csv.DictReader(act_file)
    activity_data = {(row['Id'], row['date']): row for row in act_reader}

# Read the sleep data
with open(sleep_path, 'r') as sleep_file:
    sleep_reader = csv.DictReader(sleep_file)
    sleep_data = {(row['Id'], row['date']): row for row in sleep_reader}

# Merge data based on shared 'Id' and 'date'
merged_data = []

for key, act_row in activity_data.items():
    if key in sleep_data:
        merged_row = {**act_row, **sleep_data[key]}
        merged_data.append(merged_row)

# Write merged data to a new CSV file
with open(output_path, 'w', newline='') as outfile:
    if merged_data:  # Ensure there's data to write
        fieldnames = list(merged_data[0].keys())
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in merged_data:
            writer.writerow(row)

print(f"Merged data saved to {output_path}")
