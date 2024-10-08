import pandas as pd
def OutClean(file): # Remove needless columns and cleans up data for processing
    remove = ['groupId', 'trackableId', 'sets', 'repetitions'] # Needless columns
    data = pd.read_csv(file) # Read file
    for val in remove:
        data = data.drop(val, axis = 1) # Removes columns in remove list
    data[['day','hour']] = data.utctimestamp.apply(lambda x: pd.Series(str(x).split("T"))) # Splits utctimestamp column in date and time columns. Column names are same to UniSport date and time columns
    data = data.drop('utctimestamp', axis = 1) # Remove utctimestamp column
    data.insert(0, 'day', data.pop('day')) # Set day as first column
    data.insert(1, 'hour', data.pop('hour')) # Set hour as second column
    data['day'] = pd.to_datetime(data['day']).dt.strftime('%d/%m/%Y') # Set day column values to match format of UniSport day column
    data['hour'] = pd.to_numeric(data['hour'].str[:2]) # Keep only first two digit of hour column (the actual hour) and turn the value to integer type
    data = data.groupby(['day', 'hour', 'area'])['usageMinutes'].sum() # Sum usageMinutes cells in rows with the same day, hour and area
    return data
