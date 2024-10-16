from prophet import Prophet
import pandas as pd
import os
import json

class WeekPred:
        def __init__(self, data_dir): # initializing the class and setting the base for where the data is stored
                self.data_dir = data_dir

        def select_location(self, location):
                fpath = os.path.join(self.data_dir, f"{location}")
                try: # ADD checks for having ds and y columns
                        data = pd.read_csv(fpath)
                        data['ds'] = pd.to_datetime(data['ds'])
                        return data
                except FileNotFoundError:
                        print(f"Data for location '{location}' not found at {fpath}.")
                        return None

        def aggregate_week(self, dataframe):
                dataframe['weekday'] = dataframe['ds'].dt.dayofweek #mon-sun 0-6
                dataframe['hour'] = dataframe['ds'].dt.hour

                week_schedule = dataframe.groupby(['weekday', 'hour']).y.mean().reset_index()
                return week_schedule

        def fit_prophet(self, data):

                data['ds'] = pd.to_datetime(data['weekday'] * 24 + data['hour'], unit='h')
                data = data[['ds', 'y']]
                
                model = Prophet(
                        daily_seasonality=True,
                        weekly_seasonality=True
                        )
                model.fit(data)
                return model

        def predict_week(self, model):
                week = model.make_future_dataframe(periods=168, freq='H')
                forecast = model.predict(week)

                return forecast[['ds', 'yhat']].head(168)

        def preds_to_json(self, predictions, location, output_file):

                predictions['weekday'] = predictions['ds'].dt.dayofweek
                predictions['hour'] = predictions['ds'].dt.hour

                week_forecast = []
                for _, row in predictions.iterrows():
                        week_forecast.append({
                                "weekday": int(row['weekday']),
                                "hour": int(row['hour']),
                                "pred_visitcount": float(row['yhat'])
                        })
                
                result = {
                        "location": location,
                        "week_forecast": week_forecast
                }

                with open(output_file, 'w') as f:
                        json.dump(result, f, indent=4)

        def run_for_location(self, location, output_file):
                data = self.select_location(location)
                
                if data is not None:
                        week_data = self.aggregate_week(data)

                        model = self.fit_prophet(week_data)

                        predictions = self.predict_week(model)

                        self.preds_to_json(predictions, location, output_file)
                        print(f"Predictions for location {location} saved to {output_file}.")


# for actually running this

if __name__ == "__main__":
        #directory = "C:/Users/annie/Documents/Data Science/Intro to DS" #path to the folder where data files are
        predictor = WeekPred('.')

        # select location and the file to output results into
        location = "testcounts.csv" #filename
        output_file = "testforecast.json"

        # run predictor
        predictor.run_for_location(location, output_file)

                        
