import json
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

# Load the data from filtered_baxa.json
with open('C:\Users\chris\OneDrive\Desktop\VS SleepStudy Project\OUSleep\fitabaseexampledata\filtered_data.json', 'r') as file:
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
         
            # Appending data for ML model
            X.append(list(stats.values())[:-1])  # Exclude the last value, which is the ratio we just calculated
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

# Feature importances (if you're interested in seeing which parameters are most influential)
importances = rf_regressor.feature_importances_
sorted_indices = np.argsort(importances)[::-1]

class ForestResult:
    def __init__(self, features, importances):
        self.features = features
        self.importances = importances
        
    def display_importances(self):
        for index in sorted_indices:
            print(f"{self.features[index]}: {self.importances[index]}")

result = ForestResult(features, importances)
result.display_importances()


