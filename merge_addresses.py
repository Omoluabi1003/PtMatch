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


def find_missing(staddy_csv: str, stlucie_csv: str, output_csv: str) -> None:
    """Write rows from ``stlucie_csv`` that are absent in ``staddy_csv``."""
    staddy = load_csv(staddy_csv)
    staddy = standardize_gis(staddy)

    stlucie = load_csv(stlucie_csv)

    merged = stlucie.merge(
        staddy[ADDRESS_KEY_COLUMNS].drop_duplicates(),
        on=ADDRESS_KEY_COLUMNS,
        how="left",
        indicator=True,
    )
    missing = merged[merged["_merge"] == "left_only"][STLUCIE_COLUMNS]
    missing.to_csv(output_csv, index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=(
            "Clean a StAddy export and list addresses in the St. Lucie file"
            " that do not appear in it"
        )
    )
    parser.add_argument("staddy_csv", help="StAddy export (CSV or .gz)")
    parser.add_argument("stlucie_csv", help="Existing St. Lucie CSV file")
    parser.add_argument("output_csv", help="Output CSV path for missing addresses")
    args = parser.parse_args()
    find_missing(args.staddy_csv, args.stlucie_csv, args.output_csv)
