import json
from math import sqrt

# Original weights without 'TotalMinutesAsleep'
original_weights = {
    'SedentaryMinutes': 0.24295697216178969,
    'LightlyActiveMinutes': 0.12654091586523836,
    'LightActiveDistance': 0.12263681127780418,
    'RestingHeartRate': 0.11747793387979553,
    'TotalSteps': 0.10884158091553033,
    'TotalDistance': 0.08266509015297839,
    'ModeratelyActiveDistance': 0.055884426632991716,
    'FairlyActiveMinutes': 0.050272287859597746,
    'VeryActiveDistance': 0.040042402673390404,
    'VeryActiveMinutes': 0.03400749106232626
}

# Adjust weights to make room for 'TotalMinutesAsleep'
factor = sum(original_weights.values()) / (sum(original_weights.values()) + 0.5)
weights = {k: v * factor for k, v in original_weights.items()}
weights['TotalMinutesAsleep'] = 0.5

# Adjust ideal_values
ideal_values = {
    'SedentaryMinutes': 300,
    'LightlyActiveMinutes': 180,
    'LightActiveDistance': 3,
    'RestingHeartRate': 70,
    'TotalSteps': 10000,
    'TotalDistance': 7,
    'ModeratelyActiveDistance': 2,
    'FairlyActiveMinutes': 30,
    'VeryActiveDistance': 1,
    'VeryActiveMinutes': 20,
    'TotalMinutesAsleep': 480
}

positive_parameters = ["LightlyActiveMinutes", "TotalSteps", "FairlyActiveMinutes", "VeryActiveMinutes"]

def calculate_score(key, value, ideal_value, weight, std_dev):
    deviation = (value - ideal_value) / ideal_value

    # For parameters where exceeding is positive
    #if key in positive_parameters and deviation > 0:
        # Boost score as per the number of standard deviations surpassed
        #score_boost = deviation * std_dev / ideal_value
        #return weight * (1 + score_boost)

    tolerance = 0.05  # 25% tolerance

    # Check if deviation is within tolerance
    if abs(deviation) <= tolerance:
        return weight

    # If not, square the deviation
    squared_deviation = deviation ** 2

    # Calculate score based on squared deviation
    score = weight * (1 - squared_deviation)
    
    # Ensure score stays between 0 and weight
    return max(0, min(weight, score))

# Load data from JSON
with open("updated_data.json", "r") as file:
    data = json.load(file)

# Calculate standard deviations for each parameter
std_devs = {}
for key in ideal_values:
    all_values = [daily_data[key] for user_data in data.values() for daily_data in user_data.values() if key in daily_data]
    if not all_values:  # If all_values list is empty
        std_devs[key] = 0
        continue
    mean = sum(all_values) / len(all_values)
    variance = sum((x - mean) ** 2 for x in all_values) / len(all_values)
    std_devs[key] = sqrt(variance)

# Calculate health scores for each user and date
health_scores = {}
# Calculate health scores for each user and date
health_scores = {}
for user_id, user_data in data.items():
    health_scores[user_id] = {}
    for date, daily_data in user_data.items():
        total_score = 0
        score_composition = {}
        for key, weight in weights.items():
            if key in daily_data:
                user_value = daily_data[key]
                ideal_value = ideal_values[key]
                std_dev = std_devs[key]
                score = calculate_score(key, user_value, ideal_value, weight, std_dev)
                total_score += score
                score_composition[key] = score
        
        total_score = min(total_score, 1)  # Cap the total score to a maximum of 1
        health_scores[user_id][date] = total_score

def get_score_data():
    return total_score, score_composition

# Save sleep_scores to a new JSON file
with open("sleep_scores.json", "w") as file:
    json.dump(health_scores, file, indent=4)
