# Address Dataset Preparation

Two source files are provided from St. Lucie County, Florida:

- **`ST LUCIE_2025-07-01.csv`** – the existing master list of addresses already in the St. Lucie column layout.
- **`compressed_data (1).csv.gz`** – a new export from the county GIS system that contains additional records and many extra fields.

The merge process converts the GIS export to the same column set as the master file and appends the new rows.

## Cleaning workflow

1. Decompress and load `compressed_data (1).csv.gz` using pandas.
2. Rename GIS columns to the St. Lucie column names:
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
- pandas (`requirements.txt` lists the dependency)

Install dependencies with `pip install -r requirements.txt`.

## Running the merge script

Run the provided `merge_addresses.py` script from the repository root:

```bash
python3 merge_addresses.py "ST LUCIE_2025-07-01.csv" "compressed_data (1).csv.gz" output.csv
```

The script writes `output.csv` containing all original rows followed by the
cleaned GIS records in the same St. Lucie column order.
