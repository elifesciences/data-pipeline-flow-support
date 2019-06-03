"""WARN: this code is run without a virtualenv
it must not have any dependencies other than Python3"""

import sys, json, csv, fileinput, datetime
from datetime import timezone

FILENAME_DELIMITER = '_'


def normalise(colheader):
    return colheader.lower().strip().replace(' ', '_').replace(")", "").replace("(", "")


def now():
    dtobj = datetime.datetime.now(timezone.utc)
    return dtobj.strftime("%Y-%m-%dT%H:%M:%SZ")


def first(lst):
    try:
        return lst[0]
    except IndexError:
        return None


def empty_fields_are_null(row):
    "mutator"
    for key, val in row.items():
        if isinstance(val, str) and str(val).strip() == "":
            row[key] = None
    return row


def main(input=None, output=None, filename=None):
    # fileinput.input reads sys.argv for input if we don't specify what it should be reading
    stdin = ['-']
    fh = input or fileinput.input(stdin)
    out = output or print

    time_now = now()

    header_reader = csv.reader(fh)
    header = list(map(normalise, next(header_reader)))
    if filename:
        status = filename.split(FILENAME_DELIMITER)
        status = " ".join(status[1:])
    else:
        status = ''

    reader = csv.DictReader(fh, fieldnames=header)

    for row in reader:
        row['status'] = status
        row["imported_timestamp"] = time_now

        empty_fields_are_null(row)

        out(json.dumps(row))


if __name__ == '__main__':
    args = sys.argv[1:]
    main(filename=first(args) or None)
