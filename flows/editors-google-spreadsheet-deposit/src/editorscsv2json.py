"""WARN: this code is run without a virtualenv
it must not have any dependencies other than Python3"""

import sys, json, csv, fileinput, datetime
from datetime import timezone

def normalise(colheader):
    return colheader.lower().strip().replace(" ", "_").replace(")", "").replace("(", "")


def get_utc_time(string_datetime:str):
    dtobj = datetime.datetime.strptime(string_datetime, "%Y-%m-%d %H:%M:%S %z")
    dtobj = dtobj.astimezone(tz=timezone.utc)
    return dtobj.strftime("%Y-%m-%dT%H:%M:%SZ")

def now():
    dtobj = datetime.datetime.now(timezone.utc)
    return dtobj.strftime("%Y-%m-%d %H:%M:%S %z")


def get_args(lst):
    try:
        return lst[0], lst[1]
    except IndexError:
        return None, now()


def empty_fields_are_null(row):
    "mutator"
    for key, val in row.items():
        if isinstance(val, str) and str(val).strip() == "":
            row[key] = None
    return row


def main(input=None, output=None, filename=None, time_now=None):
    # fileinput.input reads sys.argv for input if we don't specify what it should be reading
    stdin = ["-"]
    fh = input or fileinput.input(stdin)
    out = output or print

    header_reader = csv.reader(fh)
    header = list(map(normalise, next(header_reader)))
    editor_role = " ".join(filename.split('_')[1:]) if filename else ""
    reader = csv.DictReader(fh, fieldnames=header)

    for row in reader:
        row["editor_role"] = editor_role
        row["imported_timestamp"] = time_now
        empty_fields_are_null(row)

        out(json.dumps(row))


if __name__ == "__main__":
    args = sys.argv[1:]
    file_name, current_time = get_args(args)
    main(filename=file_name, current_time=current_time)
