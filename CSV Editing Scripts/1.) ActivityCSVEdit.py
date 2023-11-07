import csv
from datetime import datetime

inputpath = "Baxa_data/dailyActivity_merged.csv"
outputpath = "Baxa_data/dailyActivity_modified.csv"

# Read the CSV data from the input file
with open(inputpath, 'r') as infile:
    reader = csv.DictReader(infile)
    
    # Store modified rows in a list
    modified_data = []
    
    for row in reader:
        # Modify the 'ActivityDate' to desired format
        row["ActivityDate"] = datetime.strptime(row["ActivityDate"], "%m/%d/%Y").strftime("%m/%d/%Y")
        modified_data.append(row)

# Columns to be removed
remove_columns = ["TrackerDistance", "LoggedActivitiesDistance", "Calories", "Floors", "CaloriesBMR", "MarginalCalories"]

# Write the modified data to the new file
with open(outputpath, 'w', newline='') as outfile:
    fieldnames = [col for col in modified_data[0].keys() if col not in remove_columns]
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    
    # Write the header (rename 'ActivityDate' to 'date')
    fieldnames[fieldnames.index("ActivityDate")] = "date"
    writer.writeheader()
    
    # Write the modified rows
    for row in modified_data:
        # Remove unwanted columns
        for col in remove_columns:
            row.pop(col, None)
        # Rename 'ActivityDate' to 'date' in the row dictionary
        row["date"] = row.pop("ActivityDate")
        writer.writerow(row)

print(f"Modified data saved to {outputpath}")
