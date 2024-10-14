import requests
from bs4 import BeautifulSoup
import os
import pandas as pd

# Code to load the compressed .csv files:

url = "https://hkikanslialiikuntapaikat.z6.web.core.windows.net/ulkokuntosali/index.html" # Source url for outdoor gym usage data
os.makedirs("outfiles", exist_ok=True) # Directory to store outdoor the files

def loadcsv(): # Get the needed .csv files from the source (as we need .csv files and the source has both .csv and .json)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    for link in soup.find_all('a'): # Find all links in source page
        href = link.get('href')
        if href and href.endswith('.csv.gz') and 'hourly' in href: # Note: the files are all compressed, hence why the href needs to end in '.csv.gz'. Also 'hourly' must be in the href, as we want hourly data files
            if '2023' in href or '2024' in href: # We want data from 2023 and 2024, hence why the href must contain either one of those strings
                loadurl = 'https://hkikanslialiikuntapaikat.z6.web.core.windows.net/ulkokuntosali/' + href  # Note: url to load files is different than source page url! 
                print(f"Downloading {loadurl}...")
                csvres = requests.get(loadurl)
                csvres.raise_for_status()
                csvfile = os.path.join("outfiles", os.path.basename(href)) # .csv gets loaded in the outfiles directory
                with open(csvfile, 'wb') as f:
                    f.write(csvres.content)
                print(f"Saved {csvfile}") # Prints if loading was successful

# Code to clean the previously-loaded files:

def OutClean(file): # Remove needless columns and cleans up data for processing
    remove = ['groupId', 'trackableId', 'sets', 'repetitions'] # Needless columns
    file = pd.read_csv(file, compression = 'gzip') # Unzip and read files
    for val in remove:
        file = file.drop(val, axis = 1) # Removes columns in remove list
    file[['day','hour']] = file.utctimestamp.apply(lambda x: pd.Series(str(x).split("T"))) # Splits utctimestamp column in date and time columns. Column names are same to UniSport date and time columns
    file = file.drop('utctimestamp', axis = 1) # Remove utctimestamp column
    file.insert(0, 'day', file.pop('day')) # Set day as first column
    file.insert(1, 'hour', file.pop('hour')) # Set hour as second column
    file['day'] = pd.to_datetime(file['day']).dt.strftime('%d/%m/%Y') # Set day column values to match format of UniSport day column
    file['hour'] = pd.to_numeric(file['hour'].str[:2]) # Keep only first two digit of hour column (the actual hour) and turn the value to integer type
    file = file.groupby(['day', 'hour', 'area'])['usageMinutes'].sum() # Sum usageMinutes cells in rows with the same day, hour and area
    return file
