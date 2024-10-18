import json
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data")
locations = [
    'kluuvi', 'kumpula', #'otaniemi',
    'toolo', 'meilahti', #'Pirkkola', #'Paloheinä', #, 'Hietaniemi'
]

class Encoder:
    """
    Class responsible for encoding and decoding the chosen times, dates, and locations 
    between integer and (date, time, location) representations.
    """
    def __init__(self, available_dates, available_times, available_locations=locations):
        """Initialize the Encoder with available dates, times, and locations."""
        self.available_dates = self.flatten_list(available_dates)
        self.available_times = available_times  
        self.available_locations = available_locations  
        self.date_time_loc_to_literal = {}
        self.literal_to_date_time_loc = {}
        self.literal_groups = []  # Changed to a list to hold lists for each date
        self.date_literals = []  
        self.date_time_loc_to_checkins = {} 
        self.generate_mappings()
        self.associate_values_from_location_files()

    def flatten_list(self, nested_list):
        """Flatten a nested list into a single list."""
        if isinstance(nested_list[0], list):
            return [item for sublist in nested_list for item in sublist]
        return nested_list

    def generate_mappings(self):
        """Generate mappings between (date, time, location) and literals."""
        index = 1
        for day_idx, date_str in enumerate(self.available_dates):
            parsed_date, _ = self.parse_iso_format(date_str)
            day_times = self.available_times[day_idx]
            
            # Create a list for all literals corresponding to this date
            date_literals_for_day = []

            # Create a new list to hold literals for each time on this date
            time_literals = []

            for time in day_times:
                # Create a list for this (date, time) combination
                time_literal_group = []
                
                for loc_idx, location in enumerate(self.available_locations):
                    print(f"Mapping {(parsed_date, time, location)} -> {index}")
                    self.date_time_loc_to_literal[(parsed_date, time, location)] = index
                    self.literal_to_date_time_loc[index] = (parsed_date, time, location)
                    
                    # Add the index to the time-specific list
                    time_literal_group.append(index)
                    date_literals_for_day.append(index)
                    index += 1
                
                # Append the time-specific literals list to the overall time literals for the day
                time_literals.append(time_literal_group)
            # Append the time literals for this date to the overall literal groups
            for l in time_literals:
                self.literal_groups.append(l)
            # Append the literals for this date to the overall date literals list
            self.date_literals.append(date_literals_for_day)

    def parse_iso_format(self, iso_string):
        """Parse an ISO 8601 formatted string and return the date and time."""
        date_obj = datetime.fromisoformat(iso_string.replace('Z', '+00:00'))
        date = date_obj.strftime('%Y-%m-%d')
        time = date_obj.strftime('%H:%M')
        return date, time

    def encode(self, date_time_loc):
        """Encode a (date, time, location) tuple into an integer literal."""
        return self.date_time_loc_to_literal.get(date_time_loc)

    def decode(self, literal):
        """Decode an integer literal back into a (date, time, location) tuple."""
        if not isinstance(literal, int):
            print(f"Error: Provided literal {literal} is not an integer.")
            return None
        
        result = self.literal_to_date_time_loc.get(literal)
        
        if result is None:
            print(f"Warning: Literal {literal} does not correspond to any date-time-location mapping.")
        
        return result

    def associate_values_from_location_files(self):
        """
        Associate the predicted check-ins from location forecast files to each encoded (date, time, location).
        The value is stored in self.date_time_loc_to_checkins for each encoded (date, time, location) combination.
        """
        for (date, time, location), literal in self.date_time_loc_to_literal.items():
            # Extract weekday and hour from the date and time
            date_obj = datetime.strptime(date, '%Y-%m-%d')
            weekday = date_obj.weekday()  # 0=Monday, 6=Sunday
            hour = int(time.split(':')[0])  # Extract hour (e.g., '15:00' -> 15)

            # Read the corresponding JSON forecast file for the location
            location_file = os.path.join(DATA_PATH, f"{location}_forecast.json")
            if not os.path.exists(location_file):
                print(f"Error: Location forecast file {location_file} not found.")
                continue
            
            with open(location_file, 'r') as file:
                location_data = json.load(file)

            # Find the predicted check-ins for the matching weekday and hour
            forecast = location_data.get('week_forecast', [])
            for entry in forecast:
                if entry['weekday'] == weekday and entry['hour'] == hour:
                    checkins = entry['pred_checkins']
                    # Save check-ins as (checkins, encoded_value_of(date_time_location))
                    self.date_time_loc_to_checkins[literal] = (checkins, literal)
                    print(f"Associated {checkins} check-ins for encoded value {literal}.")
                    break

    def get_encoded_values(self):
        """Get all encoded values from the available ISO strings, times, and locations as literals."""
        encoded_values = []
        for date_literal_group in self.date_literals:
            encoded_values.extend(date_literal_group)  # Collect all literals for the final result
        return encoded_values, self.date_time_loc_to_checkins, self.literal_groups, self.date_literals

    def get_positive_intersection(self, list1, list2):
        """Get the intersection of elements in the first list with the positive elements in the second list."""
        positive_elements = [x for x in list2 if x > 0]
        return list(set(list1) & set(positive_elements))

    def decode_list(self, literals):
        """Decode a list of integer literals back into a list of (date, time, location) tuples."""
        decoded_values = [self.decode(literal) for literal in literals]
        return decoded_values
