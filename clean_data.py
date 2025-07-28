import pandas as pd
import zipfile
import os

# Define the path to the zip file and the target CSV file name
zip_filename = 'Unincorporated-Geocoded.zip'
csv_filename = 'UC.csv'
final_zip_name = 'UC.zip'

# Define the columns to keep and their new names
columns_to_keep = {
    'USER_NUMBER': 'NUMBER',
    'USER_PREDIR': 'PREDIR',
    'USER_STNAME': 'STNAME',
    'USER_STSUFFIX': 'STSUFFIX',
    'USER_POSTDIR': 'POSTDIR',
    'USER_UNITTYPE': 'UNITTYPE',
    'USER_UNITNUM': 'UNITNUM',
    'USER_MAILCITY': 'MAILCITY',
    'USER_ZIP': 'ZIP',
    'USER_ZIP_4': 'ZIP+4',
    'USER_LAT': 'LAT',
    'USER_LONG': 'LONG',
    'USER_FEATID': 'FEATID',
    'USER_COUNTYID': 'COUNTYID',
    'USER_COUNTY': 'COUNTY',
    'USER_JURISDICTION': 'JURISDICTION',
    'USER_FIRECODE': 'FIRECODE',
    'USER_POLCODE': 'POLCODE',
    'USER_EFFDATE': 'EFFDATE',
    'USER_TDTCODE': 'TDTCODE'
}

# Open the zip file
with zipfile.ZipFile(zip_filename, 'r') as zf:
    csv_in_zip = zf.namelist()[0]
    with zf.open(csv_in_zip) as f:
        reader = pd.read_csv(f, chunksize=10000, usecols=columns_to_keep.keys())

        first_chunk = True
        for chunk in reader:
            chunk.rename(columns=columns_to_keep, inplace=True)
            if first_chunk:
                chunk.to_csv(csv_filename, index=False, mode='w', header=True)
                first_chunk = False
            else:
                chunk.to_csv(csv_filename, index=False, mode='a', header=False)

# Zip the cleaned CSV file
with zipfile.ZipFile(final_zip_name, 'w', zipfile.ZIP_DEFLATED) as zf:
    zf.write(csv_filename)

print(f"Successfully created {final_zip_name} with {csv_filename} inside.")
