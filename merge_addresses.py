import argparse
import pandas as pd

STLUCIE_COLUMNS = [
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

# Columns that uniquely describe an address for comparison
ADDRESS_KEY_COLUMNS = [
    "NUMBER",
    "PREDIR",
    "STNAME",
    "STSUFFIX",
    "POSTDIR",
    "UNITTYPE",
    "UNITNUM",
    "MAILCITY",
    "ZIP",
]


def load_csv(path: str) -> pd.DataFrame:
    """Load CSV or gzipped CSV as strings."""
    compression = "gzip" if path.endswith(".gz") else None
    return pd.read_csv(path, compression=compression, dtype=str, low_memory=False)


def standardize_gis(df: pd.DataFrame) -> pd.DataFrame:
    """Rename fields and supply missing St. Lucie columns."""
    df = df.rename(columns=RENAME_MAP)
    for col in STLUCIE_COLUMNS:
        if col not in df.columns:
            df[col] = pd.NA
    df["COUNTY"] = df.get("County", pd.NA).fillna("St. Lucie")
    df["COUNTYID"] = df["COUNTYID"].fillna(111)
    return df[STLUCIE_COLUMNS]


def find_new_points(staddy_csv: str, stlucie_csv: str, output_csv: str) -> None:
    """Write rows from ``staddy_csv`` that are absent in ``stlucie_csv``."""
    staddy = load_csv(staddy_csv)
    staddy = standardize_gis(staddy)

    stlucie = load_csv(stlucie_csv)

    merged = staddy.merge(
        stlucie[ADDRESS_KEY_COLUMNS].drop_duplicates(),
        on=ADDRESS_KEY_COLUMNS,
        how="left",
        indicator=True,
    )
    new_records = merged[merged["_merge"] == "left_only"][STLUCIE_COLUMNS]
    new_records.to_csv(output_csv, index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=(
            "Clean a StAddy export and output addresses from it that "
            "are not already in the St. Lucie CSV"
        )
    )
    parser.add_argument("staddy_csv", help="StAddy export (CSV or .gz)")
    parser.add_argument("stlucie_csv", help="Existing St. Lucie CSV file")
    parser.add_argument("output_csv", help="Output CSV path for new addresses")
    args = parser.parse_args()
    find_new_points(args.staddy_csv, args.stlucie_csv, args.output_csv)
