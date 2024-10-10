import prophet import Prophet
import pandas as pd
import os

class WeekPred:
        def __init__(self, data_dir): # initializing the class and setting the base for where the data is stored
                self.data_dir = data_dir

        def select_location(self, location):
                fpath = os.path.join(self.data_dir, f"{location}.csv")
                try: # ADD checks for having ds and y columns
                        data = pd.read_csv(fpath)
                        return data
                except FileNotFoundError:
                        print(f"Data for location '{location}' not found.")
                        return None

        def fit_prophet(self, data):
                model = Prophet(
                        daily_seasonality=True,
                        weekly_seasonality=True
                        )
                model.fit(data)
                return model

        def predict_future


