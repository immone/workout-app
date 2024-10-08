import pandas as pd

def UniClean(file): # Removes column of non-unique check-ins ('quantity') from UniSport DataFrames
    file = pd.read_csv(file).drop('quantity', axis = 1)
    file['day'] = pd.to_datetime(file['day']).dt.strftime('%d/%m/%Y')
    return file
