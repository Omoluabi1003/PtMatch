import csv
import gzip

def process_files():
    stlucie_addresses = set()
    with open('StLucie.csv', 'r') as stlucie_file:
        reader = csv.reader(stlucie_file)
        header = next(reader)
        for row in reader:
            stlucie_addresses.add(tuple(row))

    with gzip.open('StAddy.csv.gz', 'rt') as staddy_file, gzip.open('PointMatch.csv.gz', 'wt', newline='') as pointmatch_file:
        reader = csv.DictReader(staddy_file)
        writer = csv.writer(pointmatch_file)

        # Write header to PointMatch.csv.gz
        writer.writerow(['NUMBER', 'PREDIR', 'STNAME', 'STSUFFIX', 'POSTDIR', 'UNITTYPE', 'UNITNUM', 'MAILCITY', 'ZIP', 'ZIP+4', 'LAT', 'LONG', 'FEATID', 'COUNTYID', 'COUNTY', 'JURISDICTION', 'FIRECODE', 'POLCODE', 'EFFDATE', 'TDTCODE'])

        for row in reader:
            staddy_address = (
                row.get('addrnum', ''),
                row.get('roadpredir', ''),
                row.get('roadname', ''),
                row.get('roadtype', ''),
                row.get('roadpostdir', ''),
                row.get('unittype', ''),
                row.get('unitid', ''),
                row.get('postcomm', ''),
                row.get('postal', ''),
                '',  # ZIP+4
                '',  # LAT
                '',  # LONG
                '',  # FEATID
                '',  # COUNTYID
                row.get('County', ''),
                row.get('municipality', ''),
                '',  # FIRECODE
                '',  # POLCODE
                row.get('created_date', ''),
                ''  # TDTCODE
            )

            if staddy_address not in stlucie_addresses:
                writer.writerow(staddy_address)

if __name__ == '__main__':
    process_files()
