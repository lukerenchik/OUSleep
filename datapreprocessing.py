import pandas as pd
import json
if __name__ == "__main__":
    df = pd.read_csv("/Users/user/PycharmProjects/OUSleep/fitabaseexampledata/DailyActivity/ID 1003_dailyActivity_20171001_20171007.csv")
    df2 = pd.read_csv("/Users/user/PycharmProjects/OUSleep/fitabaseexampledata/HeartRate/ID 1003_dailyRestingHeartRate_20171001_20171007.csv")
    df3 = pd.read_csv("/Users/user/PycharmProjects/OUSleep/fitabaseexampledata/SleepClassic/ID 1003_sleepDay_20171001_20171007.csv")

    merged_df = pd.merge(df, df2, on="Date", how="left")
    merged_df = pd.merge(merged_df, df3, on="Date", how="left")

    filtered_df = merged_df[["Date", "TotalSteps", "TotalDistance","VeryActiveMinutes","FairlyActiveMinutes","LightlyActiveMinutes","SedentaryMinutes","Calories", "TotalMinutesAsleep", "TotalTimeInBed", "RestingHeartRate_x"]]
    result_dict = filtered_df.set_index("Date").to_dict(orient="index")

    with open("filtered_data.json", "w") as json_file:
        json.dump(result_dict, json_file)