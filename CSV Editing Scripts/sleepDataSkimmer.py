import csv

inputpath = "/Users/user/PycharmProjects/Baxa_data/BaxaSleepData.csv"
outputpath = "/Users/user/PycharmProjects/Baxa_data/BaxaSleepData_filtered.csv"

# Read the CSV data from the input file
with open(inputpath, 'r') as infile:
    reader = csv.DictReader(infile)
    
    # Filter the rows based on the conditions
    filtered_data = [row for row in reader if int(row["TotalMinutesAsleep"]) != 0 and int(row["TotalTimeInBed"]) != 0]

# Write the filtered data back to a new file (or the same file if you prefer)
with open(outputpath, 'w', newline='') as outfile:
    fieldnames = ["Id", "date", "TotalSleepRecords", "TotalMinutesAsleep", "TotalTimeInBed", "TotalTimeAwake", "TotalMinutesLight", "TotalMinutesDeep", "TotalMinutesREM"]
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    
    # Write the header
    writer.writeheader()
    
    # Write the filtered rows
    for row in filtered_data:
        writer.writerow(row)

print(f"Filtered data saved to {outputpath}")
