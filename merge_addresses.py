import argparse
import pandas as pd

STLUCIE_COLUMNS = [
    'NUMBER',
    'PREDIR',
    'STNAME',
    'STSUFFIX',
    'POSTDIR',
    'UNITTYPE',
    'UNITNUM',
    'MAILCITY',
    'ZIP',
    'ZIP+4',
    'LAT',
    'LONG',
    'FEATID',
    'COUNTYID',
    'COUNTY',
    'JURISDICTION',
    'FIRECODE',
    'POLCODE',
    'EFFDATE',
    'TDTCODE',
]

RENAME_MAP = {
    'addrnum': 'NUMBER',
    'roadpredir': 'PREDIR',
    'roadname': 'STNAME',
    'roadtype': 'STSUFFIX',
    'roadpostdir': 'POSTDIR',
    'unittype': 'UNITTYPE',
    'unitid': 'UNITNUM',
    'postcomm': 'MAILCITY',
    'postal': 'ZIP',
    'municipality': 'JURISDICTION',
}


def load_gis_csv(path: str) -> pd.DataFrame:
    """Load the gzipped GIS export as strings."""
    return pd.read_csv(path, compression='gzip', dtype=str, low_memory=False)


def standardize_gis(df: pd.DataFrame) -> pd.DataFrame:
    """Rename fields and provide missing St. Lucie columns."""
    df = df.rename(columns=RENAME_MAP)
    for col in STLUCIE_COLUMNS:
        if col not in df.columns:
            df[col] = pd.NA
    df['COUNTY'] = df.get('County', pd.NA).fillna('St. Lucie')
    df['COUNTYID'] = df['COUNTYID'].fillna(111)
    return df[STLUCIE_COLUMNS]


def merge_datasets(original_csv: str, new_csv: str, output_csv: str) -> None:
    df_old = pd.read_csv(original_csv, dtype=str, low_memory=False)
    df_new = load_gis_csv(new_csv)
    df_new = standardize_gis(df_new)
    merged = pd.concat([df_old, df_new], ignore_index=True)
    merged.drop_duplicates(subset=STLUCIE_COLUMNS, inplace=True)
    merged.to_csv(output_csv, index=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Merge new GIS records into St. Lucie dataset')
    parser.add_argument('stlucie_csv', help='Existing St. Lucie CSV file')
    parser.add_argument('gis_csv', help='Gzipped GIS export')
    parser.add_argument('output_csv', help='Output CSV path')
    args = parser.parse_args()
    merge_datasets(args.stlucie_csv, args.gis_csv, args.output_csv)
