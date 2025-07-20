# Address Dataset Preparation

This repository contains two address datasets from St. Lucie County, Florida:

- **`ST LUCIE_2025-07-01.csv`** – Base address file in the St. Lucie format with 20 columns (number, street name, lat/lon, etc.).
- **`compressed_data (1).csv.gz`** – A gzipped export from the county GIS system with 55 columns.

The goal is to combine the new GIS records with the existing St. Lucie table while retaining the original column layout.

## Cleaning workflow

1. Decompress and load `compressed_data (1).csv.gz` using pandas.
2. Rename GIS columns to the St. Lucie column names:
   - `addrnum` → `NUMBER`
   - `roadpredir` → `PREDIR`
   - `roadname` → `STNAME`
   - `roadtype` → `STSUFFIX`
   - `roadpostdir` → `POSTDIR`
   - `unittype` → `UNITTYPE`
   - `unitid` → `UNITNUM`
   - `postcomm` → `MAILCITY`
   - `postal` → `ZIP`
   - `municipality` → `JURISDICTION`
3. Create any remaining St. Lucie columns (`ZIP+4`, `LAT`, `LONG`, `FEATID`, `COUNTYID`, `COUNTY`, `FIRECODE`, `POLCODE`, `EFFDATE`, `TDTCODE`) and fill them with `NA` where not supplied. `COUNTYID` is set to `111` and `COUNTY` is "St. Lucie".
4. Reorder the columns to match the existing CSV and remove duplicate rows.
5. Concatenate the cleaned GIS records with `ST LUCIE_2025-07-01.csv`.

## Required tools

- Python 3
- pandas

Install pandas with `pip install pandas` if needed.

## Running the merge script

Run the provided `merge_addresses.py` script from the repository root:

```bash
python3 merge_addresses.py "ST LUCIE_2025-07-01.csv" "compressed_data (1).csv.gz" output.csv
```

The script writes a merged file called `output.csv` containing all original St. Lucie rows followed by the cleaned GIS records.
