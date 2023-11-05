import csv

inputpath = "Baxa_data/Baxa_Filtered_Activity_Data.csv"
outputpath = "Baxa_data/Baxa_Filtered_Activity_Data.csv"

# Read the CSV data from the input file
with open(inputpath, 'r') as infile:
    reader = csv.DictReader(infile)
    
    # Filter the rows where 'TotalSteps' is not equal to 0
    filtered_data = [row for row in reader if int(row["LightlyActiveMinutes"]) != 0]

# Write the filtered data back to a new file
with open(outputpath, 'w', newline='') as outfile:
    fieldnames = filtered_data[0].keys()
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    
    # Write the header
    writer.writeheader()
    
    # Write the filtered rows
    for row in filtered_data:
        writer.writerow(row)

print(f"Filtered data saved to {outputpath}")
