import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style("whitegrid")

# Load data
merged = pd.read_csv('data/excel_copies/merged_daily_data.csv')
avg_by_day = pd.read_csv('data/excel_copies/avg_by_day.csv')

# Plot 1: Avg steps by day of week
plt.figure(figsize=(8, 6))
plt.bar(avg_by_day['DayOfWeek'], avg_by_day['TotalSteps'], color='blue')
plt.title('Average Total Steps by Day of Week')
plt.ylabel('Steps')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('data/excel_copies/avg_steps_by_day.png')
plt.close()

# Plot 2: Correlation heatmap (simple bar for now, or use seaborn if available)
# For simplicity, plot calories vs steps
plt.figure(figsize=(8, 6))
plt.scatter(merged['TotalSteps'], merged['Calories'], alpha=0.5)
plt.title('Calories vs Total Steps')
plt.xlabel('Total Steps')
plt.ylabel('Calories')
plt.tight_layout()
plt.savefig('data/excel_copies/calories_vs_steps.png')
plt.close()

# Plot 3: Avg sleep hours by day
plt.figure(figsize=(8, 6))
plt.bar(avg_by_day['DayOfWeek'], avg_by_day['TotalSleepHours'], color='green')
plt.title('Average Sleep Hours by Day of Week')
plt.ylabel('Hours')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('data/excel_copies/avg_sleep_by_day.png')
plt.close()

print("Visualizations created.")
