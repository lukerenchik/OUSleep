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

factor = sum(original_weights.values()) / (sum(original_weights.values()) + 0.5)
weights = {k: v * factor for k, v in original_weights.items()}
weights['TotalMinutesAsleep'] = 0.5


def calculate_score(user_value, ideal_value, weight, key, positive_parameters, scaling_factor=5.0):
    # Calculate deviation

    deviation = user_value - ideal_value
    # Adjust deviation using the scaling factor
    adjusted_deviation = scaling_factor * abs(deviation) / ideal_value

    # Initialize score
    score = 0

    # Check if the parameter is a positive one
    if key in positive_parameters:
        # If user value surpasses ideal, boost the score
        if deviation > 0:
            score = weight * (1 + exp(-adjusted_deviation))
        else:
            score = weight * (1 - exp(-adjusted_deviation))
    else:
        # For other parameters, score decreases with deviation
        score = weight * (1 - exp(-adjusted_deviation))

    # Ensuring score is within the range 0 to 1.5 times the weight
    return max(0, min(score, 1.5 * weight))


# Calculate standard deviations for each parameter
def calculate_sleep_scores(data):
    for key in ideal_values:
        all_values = [daily_data[key] for user_data in data.values() for daily_data in user_data.values() if
                      key in daily_data]
        if not all_values:  # If all_values list is empty
            continue

    sleep_scores = {}
    # New logic to apply lingering penalty
    prev_day_extreme_penalty_users = set()

    for user_id, user_data in data.items():
        sleep_scores[user_id] = {}
        for date, daily_data in user_data.items():
            total_score = 0
            score_composition = {}
            for key, weight in weights.items():
                if key in daily_data:
                    user_value = daily_data[key]
                    ideal_value = ideal_values[key]
                    # Calculate the score for the current key and update the total score
                    score = calculate_score(user_value, ideal_value, weight, key, positive_parameters)
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
            sleep_scores[user_id][date] = [total_score, score_composition]
    return sleep_scores


def get_sleep_scores_from_file(file_path):
    with open(file_path, "r") as file:
        data = json.load(file)
    return calculate_sleep_scores(data)


if __name__ == "__main__":
    sleep_scores = get_sleep_scores_from_file("JSON Data/updated_data.json")
    #print(sleep_scores)

# Save sleep_scores to a new JSON file
# with open("JSON DATA/sleep_scores.json", "w") as file:
#    json.dump(sleep_scores, file, indent=4)