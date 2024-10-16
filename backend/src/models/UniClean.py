import pandas as pd

def UniClean(file): # # Removes column of non-unique check-ins ('quantity') from UniSport DataFrames and puts day and hour data in one single column                                                
    filename = file
    filepath = "./unifiles/" # UniSport files are stored in a directory called 'unifiles' within the local directory the cleaner's in
    file = filepath + filename # Solves FileNotFoundError caused by the files being in a different directory than the program
    file = pd.read_csv(file).drop('quantity', axis = 1) # Remove quantity column
    file['day'] = pd.to_datetime(pd.to_datetime(file['day']).dt.strftime('%Y-%m-%d')) # Format day column to y-m-d
    file['day'] +=  pd.to_timedelta(file.hour, unit='h') # Turn hour column integers into datetime format and add it to the day column
    file = file.rename(columns = {'day':'time'}) # Rename day column to time column
    file = file.drop('hour', axis = 1) # Remove hour column
    file = file.rename(columns = {'unique_accounts_quantity':'check-ins'}) # Rename second column to check-ins
    newfile = filepath + filename[:-4] + '_clean.csv' # Generate new file name (including path)
    file.to_csv(newfile) # Write into new file
    return file
