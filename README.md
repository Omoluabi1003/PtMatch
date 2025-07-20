# Address Dataset Preparation

Two source files are provided from St. Lucie County, Florida:

- **`compressed_data (1).csv.gz`** – a StAddy export from the county GIS system. It
  contains many extra columns and uses different field names.
- **`ST LUCIE_2025-07-01.csv`** – the existing master list of addresses already
  in the St. Lucie column layout. It serves as both the template and the list
  of addresses to compare against the cleaned StAddy file.

The goal is to clean the StAddy export so its columns match the St. Lucie file
and then find all addresses that appear in the export but do not yet exist in
`ST LUCIE_2025-07-01.csv`.

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
5. Compare the cleaned records with `ST LUCIE_2025-07-01.csv` to identify rows
   present in the StAddy export that do not appear in the existing file.

## Required tools

- Python 3
- pandas (`requirements.txt` lists the dependency)

Install dependencies with `pip install -r requirements.txt`.

## Running the comparison script

Run the provided `merge_addresses.py` script from the repository root. It takes
the StAddy export followed by the St. Lucie CSV and writes a list of addresses
from the StAddy file that are not found in the existing St. Lucie data:

```bash
python3 merge_addresses.py "compressed_data (1).csv.gz" "ST LUCIE_2025-07-01.csv" PointMatch.csv
```

`PointMatch.csv` will contain only those rows from the cleaned StAddy export that
are not already listed in `ST LUCIE_2025-07-01.csv` and will follow the same
column order.
