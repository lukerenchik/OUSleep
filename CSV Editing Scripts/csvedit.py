import csv
from datetime import datetime

csvpath = "/Users/user/PycharmProjects/Baxa_data/sleepStagesDay_merged.csv"
outputpath = "/Users/user/PycharmProjects/Baxa_data/BaxaActivity.csv"

# Open the CSV file at csvpath for reading
with open(csvpath, 'r') as infile:
    reader = csv.DictReader(infile)
    
    # Create a new list for the transformed rows
    transformed_data = []
    
    for row in reader:
        # Convert the 'SleepDay' value to the desired format
        row["SleepDay"] = datetime.strptime(row["SleepDay"], "%m/%d/%Y %I:%M:%S %p").strftime("%m/%d/%Y")
        transformed_data.append(row)
    
    # Write the transformed data to a new file at outputpath
    with open(outputpath, 'w', newline='') as outfile:
        fieldnames = ["Id", "date", "TotalSleepRecords", "TotalMinutesAsleep", "TotalTimeInBed", "TotalTimeAwake", "TotalMinutesLight", "TotalMinutesDeep", "TotalMinutesREM"]
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        
        # Write the header
        writer.writeheader()
        
        # Write the transformed rows
        for row in transformed_data:
            # Rename 'SleepDay' to 'date' in the row dictionary
            row['date'] = row.pop('SleepDay')
            writer.writerow(row)

print(f"Transformed data saved to {outputpath}")
