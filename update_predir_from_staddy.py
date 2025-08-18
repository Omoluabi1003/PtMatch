import pandas as pd

# Load the datasets
p3k_df = pd.read_csv('p3k.csv', low_memory=False)
staddy_df = pd.read_csv('StAddy.csv.gz', compression='gzip', low_memory=False)

# Prepare for merging
p3k_df['NUMBER_str'] = p3k_df['NUMBER'].astype(str)
p3k_df['STNAME_lower'] = p3k_df['STNAME'].str.strip().str.lower().fillna('')
p3k_df['STSUFFIX_lower'] = p3k_df['STSUFFIX'].str.strip().str.lower().fillna('')

staddy_df['addrnum_str'] = staddy_df['addrnum'].astype(str)
staddy_df['roadname_lower'] = staddy_df['roadname'].str.strip().str.lower().fillna('')
staddy_df['roadtype_lower'] = staddy_df['roadtype'].str.strip().str.lower().fillna('')

# Create a dataframe with the predirectional information
predir_df = staddy_df[['addrnum_str', 'roadname_lower', 'roadtype_lower', 'roadpredir']].dropna(subset=['roadpredir'])
predir_df = predir_df.drop_duplicates(subset=['addrnum_str', 'roadname_lower', 'roadtype_lower'])

# Store original columns to select later
original_columns = p3k_df.columns.drop(['NUMBER_str', 'STNAME_lower', 'STSUFFIX_lower'])

# Merge the dataframes
merged_df = pd.merge(p3k_df, predir_df,
                     left_on=['NUMBER_str', 'STNAME_lower', 'STSUFFIX_lower'],
                     right_on=['addrnum_str', 'roadname_lower', 'roadtype_lower'],
                     how='left')

# Update the PREDIR column
merged_df['PREDIR'] = merged_df['roadpredir'].fillna(merged_df['PREDIR'])

# Clean up the final dataframe
merged_df = merged_df[original_columns]

# Save the updated dataframe to a new CSV file
merged_df.to_csv('PTMatch08182025.csv', index=False)

print("Successfully updated PREDIR and created PTMatch08182025.csv")
