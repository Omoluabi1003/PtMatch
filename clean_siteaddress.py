import pandas as pd

# Load the raw site address data
raw_file = 'SiteAddress08152025.csv'
output_file = 'SiteAddressPtMatch.csv'

# Columns to extract and their mapping to PointMatch schema
columns_to_keep = {
    'addrnum': 'NUMBER',
    'roadpredir': 'PREDIR',
    'roadname': 'STNAME',
    'roadtype': 'STSUFFIX',
    'roadpostdir': 'POSTDIR',
    'unittype': 'UNITTYPE',
    'unitid': 'UNITNUM',
    'postcomm': 'MAILCITY',
    'postal': 'ZIP',
    'County': 'COUNTY',
    'municipality': 'JURISDICTION',
    'created_date': 'EFFDATE'
}

# Read the CSV and select necessary columns
site_df = pd.read_csv(raw_file, dtype=str)[list(columns_to_keep.keys())]
site_df.rename(columns=columns_to_keep, inplace=True)

# Convert all fields to uppercase
site_df = site_df.applymap(lambda x: x.upper() if isinstance(x, str) else x)

# Trim EFFDATE to date-only format
site_df['EFFDATE'] = (
    pd.to_datetime(site_df['EFFDATE'], errors='coerce')
    .dt.date.astype('string')
    .fillna('')
)

# Populate constant identifiers
site_df['FEATID'] = '2403646'
site_df['COUNTYID'] = '111'
site_df['COUNTY'] = 'ST. LUCIE'
site_df['FIRECODE'] = '73'
site_df['POLCODE'] = '377'

# Ensure all expected columns exist
all_columns = ['NUMBER', 'PREDIR', 'STNAME', 'STSUFFIX', 'POSTDIR',
               'UNITTYPE', 'UNITNUM', 'MAILCITY', 'ZIP', 'ZIP+4',
               'LAT', 'LONG', 'FEATID', 'COUNTYID', 'COUNTY',
               'JURISDICTION', 'FIRECODE', 'POLCODE', 'EFFDATE', 'TDTCODE']
for col in all_columns:
    if col not in site_df:
        site_df[col] = ''
    else:
        site_df[col] = site_df[col].fillna('')

# Drop unit information and keep unique base addresses
base_cols = ['NUMBER', 'PREDIR', 'STNAME', 'STSUFFIX', 'POSTDIR', 'MAILCITY', 'ZIP']
site_df['UNITTYPE'] = ''
site_df['UNITNUM'] = ''
site_df = site_df.drop_duplicates(subset=base_cols)

# Reorder columns to match PointMatch schema
site_df = site_df[all_columns]

# Save the cleaned data
site_df.to_csv(output_file, index=False)
