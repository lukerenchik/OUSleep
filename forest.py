import json
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

# Load the data from sleepdata.json
with open('filtered_data.json', 'r') as file:
    data = json.load(file)


for date, stats in data.items():
    # Check if both keys exist in the dictionary to avoid KeyError
    if "TotalMinutesAsleep" in stats and "TotalTimeInBed" in stats:
        # Compute the ratio and add it to the dictionary
        ratio = stats["TotalMinutesAsleep"] / stats["TotalTimeInBed"]
        stats["SleepToBedRatio"] = ratio


# Optionally, to save the updated JSON data
with open("updated_data.json", "w") as f:
    json.dump(data, f, indent=4)

# Extracting input features and target variable
X = [list(day_data.values())[:-1] for day_data in data.values()]
y = [day_data["TotalMinutesAsleep"] for day_data in data.values()]


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

# Features for reference (excluding the target)
features = [
    "TotalSteps", "TotalDistance", "VeryActiveMinutes",
    "FairlyActiveMinutes", "LightlyActiveMinutes", "SedentaryMinutes", "Calories",
    "TotalMinutesAsleep", "TotalTimeInBed", "RestingHeartRate_x","SleepToBedRatio"
]

# Feature importances (if you're interested in seeing which parameters are most influential)
importances = rf_regressor.feature_importances_
sorted_indices = np.argsort(importances)[::-1]
for index in sorted_indices:
    print(f"{features[index]}: {importances[index]}")
