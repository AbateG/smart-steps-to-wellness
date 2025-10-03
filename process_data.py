import pandas as pd
import os
from datetime import datetime

# Directories
data_dir = 'data/mturkfitbit_export_4.12.16-5.12.16/Fitabase Data 4.12.16-5.12.16'
output_dir = 'data/excel_copies'
os.makedirs(output_dir, exist_ok=True)

# Load key datasets
try:
    daily_activity = pd.read_csv(os.path.join(data_dir, 'dailyActivity_merged.csv'))
except FileNotFoundError:
    print("Error: dailyActivity_merged.csv not found.")
    exit(1)

try:
    sleep_day = pd.read_csv(os.path.join(data_dir, 'sleepDay_merged.csv'))
except FileNotFoundError:
    print("Error: sleepDay_merged.csv not found.")
    exit(1)

try:
    weight_log = pd.read_csv(os.path.join(data_dir, 'weightLogInfo_merged.csv'))
except FileNotFoundError:
    print("Warning: weightLogInfo_merged.csv not found. Proceeding without weight data.")
    weight_log = pd.DataFrame()  # Empty df

# Clean daily_activity
daily_activity['ActivityDate'] = pd.to_datetime(daily_activity['ActivityDate'])
daily_activity['DayOfWeek'] = daily_activity['ActivityDate'].dt.day_name()
daily_activity['TotalActiveMinutes'] = daily_activity['VeryActiveMinutes'] + daily_activity['FairlyActiveMinutes'] + daily_activity['LightlyActiveMinutes']

# Clean sleep_day
sleep_day['SleepDay'] = pd.to_datetime(sleep_day['SleepDay'])
sleep_day['TotalSleepHours'] = sleep_day['TotalMinutesAsleep'] / 60

# Merge daily_activity and sleep_day on Id and date
daily_activity['Date'] = daily_activity['ActivityDate']
sleep_day['Date'] = sleep_day['SleepDay']
merged = pd.merge(daily_activity, sleep_day[['Id', 'Date', 'TotalSleepRecords', 'TotalMinutesAsleep', 'TotalSleepHours']], on=['Id', 'Date'], how='left')

# Handle missing sleep data
merged['TotalSleepHours'].fillna(0, inplace=True)

# Weight log: optional, merge if available
weight_log['Date'] = pd.to_datetime(weight_log['Date'])
merged = pd.merge(merged, weight_log[['Id', 'Date', 'WeightKg', 'BMI']], on=['Id', 'Date'], how='left')

# Summary stats
print("Daily Activity Summary:")
print(merged[['TotalSteps', 'TotalDistance', 'Calories', 'TotalActiveMinutes', 'TotalSleepHours']].describe())

# Avg by day of week
avg_by_day = merged.groupby('DayOfWeek')[['TotalSteps', 'Calories', 'TotalSleepHours']].mean()
print("\nAvg by Day of Week:")
print(avg_by_day)

# Correlation
correlation = merged[['TotalSteps', 'Calories', 'TotalActiveMinutes', 'TotalSleepHours']].corr()
print("\nCorrelation Matrix:")
print(correlation)

# Save processed data
merged.to_csv(os.path.join(output_dir, 'merged_daily_data.csv'), index=False)
avg_by_day.reset_index().to_csv(os.path.join(output_dir, 'avg_by_day.csv'), index=False)
correlation.to_csv(os.path.join(output_dir, 'correlation.csv'), index=False)

print("Processing complete.")
