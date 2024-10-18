from prophet import Prophet
import pandas as pd
import os
import json
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

class WeekPred:
    def __init__(self, data_dir):  # initializing the class and setting the base for where the data is stored
        self.data_dir = data_dir

    def select_location(self, location):
        fpath = os.path.join(self.data_dir, f"{location}")
        try:
            data = pd.read_csv(fpath)
            data['time'] = pd.to_datetime(data['time'])  # Ensure 'time' is in datetime format
            return data
        except FileNotFoundError:
            print(f"Data for location '{location}' not found at {fpath}.")
            return None

    def aggregate_week(self, dataframe):
        dataframe['weekday'] = dataframe['time'].dt.dayofweek  # mon-sun 0-6
        dataframe['hour'] = dataframe['time'].dt.hour
        week_schedule = dataframe.groupby(['weekday', 'hour'])['check-ins'].mean().reset_index()
        return week_schedule

    def fit_prophet(self, data):
        # Prepare the data for Prophet with required column names
        data['time'] = pd.to_datetime(data['weekday'], unit='D') + pd.to_timedelta(data['hour'], unit='h')
        data = data[['time', 'check-ins']].rename(columns={'time': 'ds', 'check-ins': 'y'})  # Rename columns
        
        model = Prophet(
            daily_seasonality=True,
            weekly_seasonality=True,
            yearly_seasonality=False
        )
        model.fit(data)
        return model

    def predict_week(self, model):
        # Extend prediction to 336 hours (2 weeks)
        week = model.make_future_dataframe(periods=168, freq='h')
        forecast = model.predict(week)
        return forecast[['ds', 'yhat']].head(168).rename(columns={'ds': 'time', 'yhat': 'check-ins'})

    def preds_to_json(self, predictions, location, output_file):
        predictions['weekday'] = predictions['time'].dt.dayofweek
        predictions['hour'] = predictions['time'].dt.hour

        week_forecast = []
        for _, row in predictions.iterrows():
            week_forecast.append({
                "weekday": int(row['weekday']),
                "hour": int(row['hour']),
                "pred_checkins": float(row['check-ins'])
            })
        
        result = {
            "location": location,
            "week_forecast": week_forecast
        }

        with open(output_file, 'w') as f:
            json.dump(result, f, indent=4)

    def plot_predictions(self, all_predictions):
        plt.figure(figsize=(12, 6))
        
        for location, predictions in all_predictions.items():
            plt.plot(predictions['time'], predictions['check-ins'], label=location)
        
        plt.title('Predicted Number of Visitors')
        plt.xlabel('Time')
        plt.ylabel('Prediction (Number of People)')
        
        # Format x-axis to show corresponding weekdays
        ax = plt.gca()
        ax.xaxis.set_major_locator(mdates.DayLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%A'))  # Display weekdays
        
        plt.xticks(rotation=45)
        plt.legend()
        plt.tight_layout()
        plt.show()

    def run_for_locations(self, locations):
        all_predictions = {}

        for location in locations:
            data = self.select_location(location)
            
            if data is not None:
                week_data = self.aggregate_week(data)

                model = self.fit_prophet(week_data)

                predictions = self.predict_week(model)

                if location in ["Hietaniemi.csv", "Paloheinä.csv", "Pirkkola.csv"]:
                    predictions['check-ins'] *= 0.3
                

                output_file = f"data/{location.split('.')[0]}_forecast.json"
                self.preds_to_json(predictions, location, output_file)
                print(f"Predictions for location {location} saved to {output_file}.")
                
                # Store predictions for plotting
                all_predictions[location] = predictions
        
        # Plot all predictions after processing all locations
        self.plot_predictions(all_predictions)

# for actually running this
if __name__ == "__main__":
    predictor = WeekPred('data/')  # Adjusting the data directory

    # List of locations (CSV files)
    locations = [
                "toolo.csv", "kluuvi.csv", 
                "kumpula.csv", "meilahti.csv", "otaniemi.csv",
                 "Paloheinä.csv", "Pirkkola.csv", #"Hietaniemi.csv",
                ]

    # Run predictor for all specified locations
    predictor.run_for_locations(locations)
