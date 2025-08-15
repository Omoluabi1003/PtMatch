"""Clean the Unincorporated-Geocoded dataset and produce UC.zip."""

import pandas as pd
import zipfile

from process_data import FIXED_CODES, date_only, to_upper


ZIP_FILENAME = "Unincorporated-Geocoded.zip"
CSV_FILENAME = "UC.csv"
FINAL_ZIP_NAME = "UC.zip"

COLUMNS_TO_KEEP = {
    "USER_NUMBER": "NUMBER",
    "USER_PREDIR": "PREDIR",
    "USER_STNAME": "STNAME",
    "USER_STSUFFIX": "STSUFFIX",
    "USER_POSTDIR": "POSTDIR",
    "USER_UNITTYPE": "UNITTYPE",
    "USER_UNITNUM": "UNITNUM",
    "USER_MAILCITY": "MAILCITY",
    "USER_ZIP": "ZIP",
    "USER_ZIP_4": "ZIP+4",
    "USER_LAT": "LAT",
    "USER_LONG": "LONG",
    "USER_FEATID": "FEATID",
    "USER_COUNTYID": "COUNTYID",
    "USER_COUNTY": "COUNTY",
    "USER_JURISDICTION": "JURISDICTION",
    "USER_FIRECODE": "FIRECODE",
    "USER_POLCODE": "POLCODE",
    "USER_EFFDATE": "EFFDATE",
    "USER_TDTCODE": "TDTCODE",
}


with zipfile.ZipFile(ZIP_FILENAME, "r") as zf:
    csv_in_zip = zf.namelist()[0]
    with zf.open(csv_in_zip) as f:
        reader = pd.read_csv(
            f, chunksize=10000, usecols=COLUMNS_TO_KEEP.keys(), dtype=str
        )

        first_chunk = True
        for chunk in reader:
            chunk.rename(columns=COLUMNS_TO_KEEP, inplace=True)
            chunk = chunk.applymap(to_upper)
            chunk["EFFDATE"] = chunk["EFFDATE"].apply(date_only)
            for col, val in FIXED_CODES.items():
                chunk[col] = val
            if first_chunk:
                chunk.to_csv(CSV_FILENAME, index=False, mode="w", header=True)
                first_chunk = False
            else:
                chunk.to_csv(CSV_FILENAME, index=False, mode="a", header=False)

with zipfile.ZipFile(FINAL_ZIP_NAME, "w", zipfile.ZIP_DEFLATED) as zf:
    zf.write(CSV_FILENAME)

print(f"Successfully created {FINAL_ZIP_NAME} with {CSV_FILENAME} inside.")
