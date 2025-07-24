import pandas as pd
import argparse
import os

parser = argparse.ArgumentParser(description="Filter for Unincorporated Jurisdiction")
parser.add_argument("input_csv", help="Input CSV file (can be .gz)")
parser.add_argument("output_csv", help="Output CSV file")
args = parser.parse_args()

compression = 'gzip' if args.input_csv.endswith('.gz') else None

df = pd.read_csv(args.input_csv, compression=compression)
if 'JURISDICTION' not in df.columns:
    raise SystemExit("Input CSV must contain a JURISDICTION column")

mask = df['JURISDICTION'].str.contains('UNINCORPORATED', case=False, na=False)
filtered = df[mask]

filtered.to_csv(args.output_csv, index=False)
