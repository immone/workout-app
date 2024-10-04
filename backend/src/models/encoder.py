from datetime import datetime

class Encoder:
    def __init__(self, available_dates, available_times):
        """Initialize the Encoder with available dates and times."""
        self.available_dates = self.flatten_list(available_dates)
        self.available_times = available_times  # Keep as-is, since they are already nested lists
        self.date_time_to_literal = {}
        self.literal_to_date_time = {}
        self.generate_mappings()

    def flatten_list(self, nested_list):
        """Flatten a nested list into a single list."""
        if isinstance(nested_list[0], list):
            return [item for sublist in nested_list for item in sublist]
        return nested_list

    def generate_mappings(self):
        """Generate mappings between (date, time) and literals."""
        index = 1
        for day_idx, date_str in enumerate(self.available_dates):
            parsed_date, _ = self.parse_iso_format(date_str)
            day_times = self.available_times[day_idx]  # Now treat day_times as a list of full time strings
            
            for time in day_times:
                # Ensure we are mapping (date, full time string)
                print(f"Mapping {(parsed_date, time)} -> {index}")
                self.date_time_to_literal[(parsed_date, time)] = index
                self.literal_to_date_time[index] = (parsed_date, time)
                index += 1

    def parse_iso_format(self, iso_string):
        """
        Parse an ISO 8601 formatted string and return the date and time.
        
        Args:
            iso_string (str): An ISO 8601 formatted date-time string.
        
        Returns:
            tuple: A tuple (date, time) in 'YYYY-MM-DD' and 'HH:MM' format.
        """
        date_obj = datetime.fromisoformat(iso_string.replace('Z', '+00:00'))
        date = date_obj.strftime('%Y-%m-%d')  # Extract date in YYYY-MM-DD format
        time = date_obj.strftime('%H:%M')     # Extract time in HH:MM format
        return date, time

    def encode(self, date_time):
        """
        Encode a date-time tuple into an integer literal.

        Args:
            date_time (tuple): A tuple of (date, time).

        Returns:
            int: The corresponding integer literal.
        """
        return self.date_time_to_literal.get(date_time)

    def decode(self, literal):
        """
        Decode an integer literal back into a date-time tuple.

        Args:
            literal (int): The integer literal to decode.

        Returns:
            tuple: The corresponding (date, time) tuple or None if the literal is invalid.
        """
        if not isinstance(literal, int):
            print(f"Error: Provided literal {literal} is not an integer.")
            return None
        
        result = self.literal_to_date_time.get(literal)
        
        if result is None:
            print(f"Warning: Literal {literal} does not correspond to any date-time mapping.")
        
        return result

    def get_encoded_values(self):
        """
        Get all encoded values from the available ISO strings as literals.

        Returns:
            list: A list of encoded integer literals.
        """
        encoded_values = []
        for day_idx, date_time_str in enumerate(self.available_dates):
            parsed_date, _ = self.parse_iso_format(date_time_str)
            day_times = self.available_times[day_idx]  # Iterate over full time values, not characters
            
            for time in day_times:
                print(f"Trying to encode: {(parsed_date, time)}")
                encoded_value = self.encode((parsed_date, time))
                print(f"Encoded value: {encoded_value}")
                
                if encoded_value:
                    encoded_values.append(encoded_value)
        return encoded_values

    def get_positive_intersection(self, list1, list2):
        """
        Get the intersection of elements in the first list with the positive elements in the second list.

        Args:
            list1 (list): The first list of elements.
            list2 (list): The second list, which may contain positive elements.

        Returns:
            list: A list containing the intersection.
        """
        # Filter positive elements from the second list
        positive_elements = [x for x in list2 if x > 0]
        # Return the intersection with the first list
        return list(set(list1) & set(positive_elements))

    def decode_list(self, literals):
        """
        Decode a list of integer literals back into a list of date-time tuples.

        Args:
            literals (list): A list of integer literals to decode.

        Returns:
            list: A list containing the decoded (date, time) tuples or None for invalid literals.
        """
        decoded_values = [self.decode(literal) for literal in literals]
        return decoded_values
