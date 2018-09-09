import csv
import gzip
import os
import re
import subprocess

from hasher import get_salt, hash_string

FORBIDDEN_FIELDS = [
    'APPNAME',
    'EMAIL',
    'PRIMCONTNO',
    'OTHERCONTNO',
    'RESADDRESS',
    'IDNO',
    'DOB',
]
HASH_FIELD = 'HASHED_IDNO'
POST_CODE_FIELD = 'POSTALCODE'
FILTER_FIELD = 'REQTYPE'


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
    row[HASH_FIELD] = hash_string(row['IDNO'], SALT)
    return row


PATTERN = re.compile('[0-9]{5,6}')
BAD_PATTERN = re.compile('[0-9]{7}')

def anonymise_post_code(post_code):
    post_code = post_code.replace(' ', '')
    bad_match = re.search(BAD_PATTERN, post_code)
    if bad_match is not None:
        return None
    match = re.search(PATTERN, post_code)
    if match is not None:
        return match.group(0)[0:2]


def run(filename):
    with open(filename, 'rU') as read_csv, gzip.open(filename + '.gz', 'wt') as write_csv:
        reader = csv.DictReader(read_csv)
        writer = None
        for row in reader:
            if writer is None:
                writer = set_header(row, write_csv)
            row[POST_CODE_FIELD] = anonymise_post_code(row[POST_CODE_FIELD])
            row = hash_idno(row)
            row = clean_row(row, FORBIDDEN_FIELDS)
            if row[FILTER_FIELD] == 'LC':
                writer.writerow(row)


if __name__ == '__main__':
    run('lc_applicant.csv')

