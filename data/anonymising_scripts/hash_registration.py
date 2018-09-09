import csv
import gzip
import os
import re

from hasher import get_salt, hash_string

FORBIDDEN_FIELDS = [
    'ID Number',
]
HASH_FIELD = 'HASHED_IDNO'


def set_header(row, write_csv):
    header = list(row.keys())
    for field in FORBIDDEN_FIELDS:
        if field in header:
            header.remove(field)
    header.append(HASH_FIELD)
    writer = csv.DictWriter(write_csv, fieldnames=header)
    writer.writeheader()
    return writer

SALT = get_salt()

def clean_fields(row):
    return row


def clean_row(row, remove_fields):
    for field in remove_fields:
        row.pop(field)
    row = clean_fields(row)
    return row


def hash_idno(row):
    row[HASH_FIELD] = hash_string(row['ID Number'], SALT)
    return row


def run(filename):
    with open(filename, 'rU') as read_csv, gzip.open(filename + '.gz', 'wt') as write_csv:
        reader = csv.DictReader(read_csv)
        writer = None
        for row in reader:
            if writer is None:
                writer = set_header(row, write_csv)
            row = hash_idno(row)
            row = clean_row(row, FORBIDDEN_FIELDS)
            writer.writerow(row)


if __name__ == '__main__':
    run('lc_registration_cut.csv')

