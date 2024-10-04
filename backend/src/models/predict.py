import pandas as pd
from prophet import Prophet
import json
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Set random seed for reproducibility
np.random.seed(42)

# Create a date range (1 day of hourly data)
start_date = datetime(2024, 1, 1)
end_date = start_date + timedelta(days=3)  # Adjust to 3 days for a shorter time span
date_range = pd.date_range(start_date, end_date, freq='H')

# Generate mock data
n = len(date_range)
trend = np.linspace(50, 300, n)  # Linear trend from 50 to 300
seasonality = 40 * np.sin(np.linspace(0, 3 * np.pi, n))  # Seasonal component
noise = np.random.normal(0, 10, n)  # Random noise

# Final value for each hour, rounding to positive integers
y = np.maximum(0, np.round(trend + seasonality + noise)).astype(int)

# Create a DataFrame
df = pd.DataFrame({
    'ds': date_range,
    'y': y
})

# Save to CSV (optional)
#df.to_csv('mock_hourly_data.csv', index=False)

# Display the first few rows of the DataFrame
print(df.head())

# Step 2: Fit the Prophet model
model = Prophet()
model.fit(df)

# Create a future DataFrame for predictions (next 48 hours)
future = model.make_future_dataframe(periods=48, freq='H')
forecast = model.predict(future)

predictions = {}
for i in range(len(forecast)):
    day = forecast['ds'][i].strftime('%Y-%m-%d')
    hour = forecast['ds'][i].strftime('%H')
    if day not in predictions:
        predictions[day] = {}
    predictions[day][hour] = int(forecast['yhat'][i])

# Save to a JSON file
json_file_path = 'hourly_predictions.json'

with open(json_file_path, 'w') as json_file:
    json.dump(predictions, json_file, indent=4)

# Step 3: Plot the original data and the forecast
plt.figure(figsize=(14, 7))

# Original data
plt.subplot(2, 1, 1)
plt.plot(df['ds'], df['y'], label='Original Data', color='blue')
plt.plot(forecast['ds'], forecast['yhat'], label='Predicted Data', color='orange')
plt.fill_between(forecast['ds'], forecast['yhat_lower'], forecast['yhat_upper'], 
                 color='orange', alpha=0.2, label='Uncertainty Interval')
plt.title('Hourly Visitors - Original vs. Predicted Data')
plt.xlabel('Date')
plt.ylabel('Number of Visitors')
plt.legend()
plt.xticks(rotation=45)
plt.grid()

# Step 4: Plot forecasted projections as a bar plot
plt.subplot(2, 1, 2)
bar_width = 0.4  # Adjust bar width
plt.bar(forecast['ds'], forecast['yhat'].astype(int), 
        width=bar_width, color='green', alpha=0.6, label='Projected Visitors (Discretized Integers)')
plt.title('Projected Visitors per Hour (Discretized Integer Counts)')
plt.xlabel('Date')
plt.ylabel('Number of Visitors (Integers)')
plt.xticks(rotation=45)

# Add gridlines and set y-ticks at larger intervals for clarity
plt.grid()

# Set y-ticks at intervals of 50 for less crowding
plt.yticks(np.arange(0, forecast['yhat'].max() + 50, 50))

# Annotate every 12th bar for clarity
for index, value in enumerate(forecast['yhat']):
    if index % 12 == 0:  # Annotate only every 12th bar
        plt.text(forecast['ds'].iloc[index], value + 1, str(int(value)), 
                 ha='center', va='bottom', fontsize=8)

plt.legend()
plt.tight_layout()
plt.show()

