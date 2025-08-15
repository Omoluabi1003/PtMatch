import csv
import gzip

FIXED_CODES = {
    'FEATID': '2403646',
    'COUNTYID': '111',
    'COUNTY': 'ST. LUCIE',
    'FIRECODE': '73',
    'POLCODE': '377',
}


def to_upper(value: str) -> str:
    return value.upper() if isinstance(value, str) else value


def date_only(value: str) -> str:
    if not value:
        return ''
    return value.split('T')[0].split(' ')[0]


def build_row(row: dict) -> tuple:
    return (
        to_upper(row.get('addrnum', '')),
        to_upper(row.get('roadpredir', '')),
        to_upper(row.get('roadname', '')),
        to_upper(row.get('roadtype', '')),
        to_upper(row.get('roadpostdir', '')),
        '',  # UNITTYPE
        '',  # UNITNUM
        to_upper(row.get('postcomm', '')),
        to_upper(row.get('postal', '')),
        '',  # ZIP+4
        '',  # LAT
        '',  # LONG
        FIXED_CODES['FEATID'],
        FIXED_CODES['COUNTYID'],
        FIXED_CODES['COUNTY'],
        to_upper(row.get('municipality', '')),
        FIXED_CODES['FIRECODE'],
        FIXED_CODES['POLCODE'],
        date_only(row.get('created_date', '')),
        '',  # TDTCODE
    )


def build_existing_row(row: dict) -> tuple:
    return (
        to_upper(row.get('NUMBER', '')),
        to_upper(row.get('PREDIR', '')),
        to_upper(row.get('STNAME', '')),
        to_upper(row.get('STSUFFIX', '')),
        to_upper(row.get('POSTDIR', '')),
        '',  # UNITTYPE
        '',  # UNITNUM
        to_upper(row.get('MAILCITY', '')),
        to_upper(row.get('ZIP', '')),
        '',  # ZIP+4
        '',  # LAT
        '',  # LONG
        FIXED_CODES['FEATID'],
        FIXED_CODES['COUNTYID'],
        FIXED_CODES['COUNTY'],
        to_upper(row.get('JURISDICTION', '')),
        FIXED_CODES['FIRECODE'],
        FIXED_CODES['POLCODE'],
        date_only(row.get('EFFDATE', '')),
        '',  # TDTCODE
    )


def process_files():
    stlucie_addresses = set()
    with open('StLucie.csv', 'r') as stlucie_file:
        reader = csv.DictReader(stlucie_file)
        for row in reader:
            stlucie_addresses.add(build_existing_row(row))

    with gzip.open('StAddy.csv.gz', 'rt') as staddy_file, gzip.open(
        'PointMatch.csv.gz', 'wt', newline=''
    ) as pointmatch_file:
        reader = csv.DictReader(staddy_file)
        writer = csv.writer(pointmatch_file)

        # Write header to PointMatch.csv.gz
        writer.writerow([
            'NUMBER',
            'PREDIR',
            'STNAME',
            'STSUFFIX',
            'POSTDIR',
            'UNITTYPE',
            'UNITNUM',
            'MAILCITY',
            'ZIP',
            'ZIP+4',
            'LAT',
            'LONG',
            'FEATID',
            'COUNTYID',
            'COUNTY',
            'JURISDICTION',
            'FIRECODE',
            'POLCODE',
            'EFFDATE',
            'TDTCODE',
        ])

        for row in reader:
            staddy_address = build_row(row)
            if staddy_address not in stlucie_addresses:
                writer.writerow(staddy_address)


if __name__ == '__main__':
    process_files()
