import json
import pandas as pd

health_score_data_file = "OUSleep\\JSON Data\\health_scores.json"

# Define the column names in the CSV file
columns = ["Id", "date", "HealthScore"]

# Read the CSV file into a DataFrame, specifying the columns to use
health_score_df = pd.read_csv(health_score_data_file, usecols=columns)

# Now, health_score_df contains your health score data.