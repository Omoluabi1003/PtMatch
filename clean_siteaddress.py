"""Clean and standardize the SiteAddress data for PointMatch."""

from typing import Dict, List

import pandas as pd

from process_data import FIXED_CODES, date_only, to_upper


RAW_FILE = "SiteAddress08152025.csv"
OUTPUT_FILE = "SiteAddressPtMatch.csv"

# Columns to extract and their mapping to PointMatch schema
COLUMNS_TO_KEEP: Dict[str, str] = {
    "addrnum": "NUMBER",
    "roadpredir": "PREDIR",
    "roadname": "STNAME",
    "roadtype": "STSUFFIX",
    "roadpostdir": "POSTDIR",
    "unittype": "UNITTYPE",
    "unitid": "UNITNUM",
    "postcomm": "MAILCITY",
    "postal": "ZIP",
    "County": "COUNTY",
    "municipality": "JURISDICTION",
    "created_date": "EFFDATE",
}

ALL_COLUMNS: List[str] = [
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


def clean_siteaddress(raw_file: str = RAW_FILE, output_file: str = OUTPUT_FILE) -> None:
    """Read raw site address CSV and produce a normalized PointMatch file."""

    site_df = pd.read_csv(raw_file, dtype=str)[list(COLUMNS_TO_KEEP.keys())]
    site_df.rename(columns=COLUMNS_TO_KEEP, inplace=True)

    site_df = site_df.applymap(to_upper)
    site_df["EFFDATE"] = site_df["EFFDATE"].apply(date_only)

    for col, val in FIXED_CODES.items():
        site_df[col] = val

    for col in ALL_COLUMNS:
        if col not in site_df:
            site_df[col] = ""
        else:
            site_df[col] = site_df[col].fillna("")

    base_cols = [
        "NUMBER",
        "PREDIR",
        "STNAME",
        "STSUFFIX",
        "POSTDIR",
        "MAILCITY",
        "ZIP",
    ]
    site_df["UNITTYPE"] = ""
    site_df["UNITNUM"] = ""
    site_df = site_df.drop_duplicates(subset=base_cols)

    site_df = site_df[ALL_COLUMNS]
    site_df.to_csv(output_file, index=False)


if __name__ == "__main__":
    clean_siteaddress()

