import json
from math import sqrt, exp

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


def calculate_score(user_value, ideal_value, weight, std_dev):
    score = 0
    if ideal_value == 480:  # If we are evaluating "TotalMinutesAsleep"
        if user_value < 180:
            score = -2 * weight  # Extreme penalty for less than 3 hours
        elif user_value < 300:
            score = -weight  # Heavy penalty for less than 5 hours
        else:
            score = weight * min(1, user_value / ideal_value)
    else:
        z = (user_value - ideal_value) / std_dev
        if key in ['LightlyActiveMinutes', 'TotalSteps', 'FairlyActiveMinutes', 'VeryActiveMinutes']:
            if user_value > ideal_value:
                score = weight * (1 + exp(-z))
            else:
                score = weight * (1 - exp(z))
        else:
            score = weight * (1 - exp(z))
    return min(max(score, 0), weight)


# Load data from JSON, calculate standard deviations, and the rest remains the same...
# Load data from JSON
with open("JSON Data/updated_data.json", "r") as file:
    data = json.load(file)

# Calculate standard deviations for each parameter
std_devs = {}
for key in ideal_values:
    all_values = [daily_data[key] for user_data in data.values() for daily_data in user_data.values() if
                  key in daily_data]
    if not all_values:  # If all_values list is empty
        std_devs[key] = 0
        continue
    mean = sum(all_values) / len(all_values)
    variance = sum((x - mean) ** 2 for x in all_values) / len(all_values)
    std_devs[key] = sqrt(variance)

health_scores = {}
# New logic to apply lingering penalty
prev_day_extreme_penalty_users = set()

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

                # Calculate the score for the current key and update the total score
                score = calculate_score(user_value, ideal_value, weight, std_dev)
                total_score += score
                score_composition[key] = score

                # Check if the user gets extreme penalty for the current day
                if key == 'TotalMinutesAsleep' and user_value < 180:
                    prev_day_extreme_penalty_users.add(user_id)

        # Check for lingering penalty from the previous day
        if user_id in prev_day_extreme_penalty_users:
            total_score -= 2 * weights['TotalMinutesAsleep']
            prev_day_extreme_penalty_users.remove(user_id)

        # Cap the total score to a maximum of 1
        total_score = min(total_score, 1)
        health_scores[user_id][date] = total_score


def get_score_data():
    return total_score, score_composition


# Save sleep_scores to a new JSON file
with open("JSON DATA/sleep_scores.json", "w") as file:
    json.dump(health_scores, file, indent=4)
