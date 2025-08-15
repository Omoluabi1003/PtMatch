import argparse
from typing import List

import pandas as pd

from process_data import FIXED_CODES, date_only, to_upper


STLUCIE_COLUMNS: List[str] = [
    "NUMBER",
    "PREDIR",
    "STNAME",
    "STSUFFIX",
    "POSTDIR",
    "UNITTYPE",
    "UNITNUM",
    "MAILCITY",
    "ZIP",
    "ZIP+4",
    "LAT",
    "LONG",
    "FEATID",
    "COUNTYID",
    "COUNTY",
    "JURISDICTION",
    "FIRECODE",
    "POLCODE",
    "EFFDATE",
    "TDTCODE",
]

RENAME_MAP = {
    "addrnum": "NUMBER",
    "roadpredir": "PREDIR",
    "roadname": "STNAME",
    "roadtype": "STSUFFIX",
    "roadpostdir": "POSTDIR",
    "unittype": "UNITTYPE",
    "unitid": "UNITNUM",
    "postcomm": "MAILCITY",
    "postal": "ZIP",
    "municipality": "JURISDICTION",
}


def load_gis_csv(path: str) -> pd.DataFrame:
    """Load the gzipped GIS export."""
    return pd.read_csv(path, compression="gzip", dtype=str)


def normalize_df(df: pd.DataFrame) -> pd.DataFrame:
    df = df.applymap(to_upper)
    if "EFFDATE" in df.columns:
        df["EFFDATE"] = df["EFFDATE"].apply(date_only)
    if "JURISDICTION" in df.columns:
        df["JURISDICTION"] = (
            df["JURISDICTION"].fillna("UNINCORPORATED").replace("", "UNINCORPORATED")
        )
    for col, val in FIXED_CODES.items():
        if col in df.columns:
            df[col] = val
    return df


def standardize_gis(df: pd.DataFrame) -> pd.DataFrame:
    """Convert GIS columns to the St. Lucie format."""
    df = df.rename(columns=RENAME_MAP)
    for col in STLUCIE_COLUMNS:
        if col not in df.columns:
            df[col] = pd.NA
    df = normalize_df(df)
    return df[STLUCIE_COLUMNS]


def merge_datasets(original_csv: str, new_csv: str, output_csv: str) -> None:
    df_old = normalize_df(pd.read_csv(original_csv, dtype=str))
    df_new = load_gis_csv(new_csv)
    df_new = standardize_gis(df_new)
    merged = pd.concat([df_old, df_new], ignore_index=True)
    merged.drop_duplicates(inplace=True)
    merged.to_csv(output_csv, index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Merge new GIS records into St. Lucie dataset"
    )
    parser.add_argument("stlucie_csv", help="Existing St. Lucie CSV file")
    parser.add_argument("gis_csv", help="Gzipped GIS export")
    parser.add_argument("output_csv", help="Output CSV path")
    args = parser.parse_args()
    merge_datasets(args.stlucie_csv, args.gis_csv, args.output_csv)
