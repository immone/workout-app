import requests
from bs4 import BeautifulSoup
import os
import pandas as pd

# Code to load the compressed .csv files:

url = 'https://hkikanslialiikuntapaikat.z6.web.core.windows.net/ulkokuntosali/index.html' # Source url for outdoor gym usage data
os.makedirs("outraw", exist_ok=True) # Directory to store the outdoor gym files

def loadcsv(): # Get the needed .csv files from the source (as we need .csv files and the source has both .csv and .json)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    for link in soup.find_all('a'): # Find all links in source page
        href = link.get('href')
        if href and href.endswith('.csv.gz') and 'hourly' in href: # Note: the files are all compressed, hence why the href needs to end in '.csv.gz'. Also 'hourly' must be in the href, as we want hourly data files
            if '2023' in href or '2024' in href: # We want data from 2023 and 2024, hence why the href must contain either one of those strings
                loadurl = 'https://hkikanslialiikuntapaikat.z6.web.core.windows.net/ulkokuntosali/' + href  # Note: url to load files is different than source page url! 
                print(f'Downloading {loadurl}...')
                csvres = requests.get(loadurl)
                csvres.raise_for_status()
                csvfile = os.path.join('outraw', os.path.basename(href)) # .csv gets loaded in the outfiles directory
                with open(csvfile, 'wb') as f:
                    f.write(csvres.content)
                print(f"Saved {csvfile}") # Prints if loading was successful

# Code to clean the previously-loaded files:

def OutClean(file): # Remove needless columns and cleans up data for processing
    filename = file
    filepath = './outraw/' # UniSport files are stored in a directory called 'outfiles' within the local directory the cleaner's in
    file = filepath + filename # Solves FileNotFoundError caused by the files being in a different directory than the program
    remove = ['groupId', 'trackableId', 'sets', 'repetitions'] # Needless columns
    file = pd.read_csv(file) # Unzip and read file with pandas                                                                                              
    file = file.drop(columns = remove, axis = 1) # Removes columns in remove list                                                                          
    file['utctimestamp'] = (file['utctimestamp'].str.replace('T', ' ')).str.replace('.000Z', '') # Remove T within string, milliseconds and Z at end of string
    os.makedirs("outclean", exist_ok=True) # Directory to store the clean outdoor gym files
    file = file.groupby(['utctimestamp', 'area'])['usageMinutes'].sum().reset_index() # Sum usageMinutes cells in rows with the same day, hour and area
    file = file.rename(columns = {'utctimestamp':'DS', 'usageMinutes':'Y'}) # Rename utctimestamp to DS
    areas = file['area'].unique() # Find all unique values of areas
    for a in areas: # For each unique area value
        areaset = file[file['area'] == a] # Create subset for said area
        areaset = areaset.drop(columns = 'area', axis = 1) # Remove area column (we don't need it)
        newpath = './outclean/' # Path to clean data folder
        newfile = newpath + filename[:-7] + '_' + a + '_clean.csv' # Generate new file name specifying area (including path)
        areaset.to_csv(newfile) # Write into new file
    return file

if __name__ == '__main__':
    loadcsv()
    for i in os.listdir('./outraw/'):
        OutClean(i)
