"""hypothesis to bigquery

WARN: this code is run without a virtualenv
it must not have any dependencies other than Python3"""

import sys, json
from datetime import datetime

def first(lst):
    try:
        return lst[0]
    except IndexError:
        return None

def normalise_dt(dt):
    "returns a TZ aware UTC datetime object"
    # python < 3.7 cannot handle formatting timezones with a colon in it
    dt, tz = dt[:-6], dt[-6:]
    dt += tz.replace(':', '')
    return datetime.strptime(dt, "%Y-%m-%dT%H:%M:%S.%f%z")

def format_dt(dt, pattern=None):
    pattern = pattern or "%Y-%m-%dT%H:%M:%SZ" # 2019-01-24T15:45:51Z
    return datetime.strftime(dt, pattern)

def process_row(row):
    created = normalise_dt(row['created'])
    updated = normalise_dt(row['updated'])
    row = {
        "id": row['id'],
        "display_name": row['user_info']['display_name'],
        "user_email": row['user'][len("acct:"):], # "acct:g7izfhhj@elifesciences.org" => "g7izfhhj@elifesciences.org"
        "uri": row['uri'],
        "text": row['text'],
        "tags": row['tags'],
        "link_to_json": row['links']['json'],
        "link_to_incontext": row['links']['incontext'],
        "hidden": row['hidden'],
        "publisher_group": row['group'],
        "flagged": row['flagged'],
        #"title": first(row['document'].get('title', [])), # probably want this rather than what we have
        "title": row['document'].get('title', []),

        "created_time": format_dt(created, "%H:%M:%S"),
        "created_timezone": format_dt(created, "%z"),
        "created_date": format_dt(created, "%Y-%m-%d"),
        "created_datetime": format_dt(created),
        
        "updated_time": format_dt(updated, "%H:%M:%S"),
        "updated_timezone": format_dt(updated, "%z"),
        "updated_date": format_dt(updated, "%Y-%m-%d"),
        "updated_datetime": format_dt(updated)
    }
    return json.dumps(row)

def main(iinput=None, out=None):
    # fileinput.input reads sys.argv for input if we don't specify what it should be reading
    fh = open(input, 'r') if iinput else sys.stdin
    out = out or print
    data = json.loads(fh.read())
    [out(process_row(row)) for row in data['rows']]

if __name__ == '__main__':
    main()
