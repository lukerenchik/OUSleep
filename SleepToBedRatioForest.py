import json
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

# Load the data from filtered_baxa.json
with open('filtered_baxa.json', 'r') as file:
    data = json.load(file)

# Lists to collect data for machine learning
X = []
y = []

for user_id, dates in data.items():
    for date, stats in dates.items():
        # Check if both keys exist in the dictionary to avoid KeyError
        if "TotalMinutesAsleep" in stats and "TotalTimeInBed" in stats:
            # Compute the ratio and add it to the dictionary
            ratio = stats["TotalMinutesAsleep"] / stats["TotalTimeInBed"]
            stats["SleepToBedRatio"] = ratio
            
            # Remove the unwanted features for ML model input
            reduced_stats = {k: v for k, v in stats.items() if k not in ["TotalMinutesAsleep", "TotalTimeInBed", "SleepToBedRatio"]}
            
            # Appending data for ML model
            X.append(list(reduced_stats.values()))
            y.append(stats["SleepToBedRatio"])

# Optionally, to save the updated JSON data
with open("updated_data.json", "w") as f:
    json.dump(data, f, indent=4)

# Splitting data into training and testing set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initializing Random Forest Regressor
rf_regressor = RandomForestRegressor(n_estimators=100, random_state=42)

# Fitting the model
rf_regressor.fit(X_train, y_train)

# Making predictions
y_pred = rf_regressor.predict(X_test)

# Evaluating the model
mse = mean_squared_error(y_test, y_pred)
print(f"Mean Squared Error: {mse}")

# This will generate features list dynamically based on one of the data entries.
# This assumes that all data entries have the same keys.
sample_user_id = list(data.keys())[0]
sample_date = list(data[sample_user_id].keys())[0]
features = list(data[sample_user_id][sample_date].keys())
features.remove("SleepToBedRatio")
features.remove("TotalMinutesAsleep")
features.remove("TotalTimeInBed")

# Feature importances (if you're interested in seeing which parameters are most influential)
importances = rf_regressor.feature_importances_
sorted_indices = np.argsort(importances)[::-1]
for index in sorted_indices:
    print(f"{features[index]}: {importances[index]}")
