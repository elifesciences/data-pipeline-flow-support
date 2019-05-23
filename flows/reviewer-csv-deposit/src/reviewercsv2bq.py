"""reviewers csv to bigquery

WARN: this code is run without a virtualenv
it must not have any dependencies other than Python3"""

import re
import json
import sys

NUM_COLS = 5 # number of columns in csv
DELIMITER = "\",\"" #delimiter for splitting csv file rows

tag_re = re.compile(r"<.?table[^>]*>|<.?t[rd]>|<font[^>]+>|<.?b>|<.?p[^>]*>|\t") #removes html  tags from row


def parse_row(row):
    splited_values = tag_re.sub('', row).split(DELIMITER)
    splited_values_length = len(splited_values)

    # heuristics used for merging splits when the total number of split < NUM_COLS
    if splited_values_length < NUM_COLS:
        return None

    def process_last_element(text):
        text = text[:text.rfind('\"')]
        if text[0:4].upper() == 'NONE':
            return 'None' + text[4:]
        return text

    parsed_row = [None] * NUM_COLS
    parsed_row[0] = splited_values[0][1:]
    parsed_row[1] = splited_values[1]
    parsed_row[4] = process_last_element(splited_values[-1])

    # heuristics used for merging splits when the total number of split > NUM_COLS
    right_item_indices = [0, 1]
    if splited_values_length > 5:
        if sum([a.strip()[0:1].isupper() for a in splited_values[2:-1]]) == 2:
            right_item_indices = [i for i, e in enumerate([a.strip()[0:1].isupper() for a in splited_values[2:-1]])
                                  if e]
        elif sum([a.strip()[0:1].isupper() or a.strip()[0:1].isdigit() for a in splited_values[2:-1]]) == 2:
            right_item_indices = [i for i, e in enumerate(
                [a.strip()[0:1].isupper() or a.strip()[0:1].isdigit() for a in splited_values[2:-1]]) if e]

    parsed_row[2] = DELIMITER.join(splited_values[2:2 + right_item_indices[1]])
    parsed_row[3] = DELIMITER.join(splited_values[2 + right_item_indices[1]:-1])

    return parsed_row


def main(iinput=None, out=None):
    # fileinput.input reads sys.argv for input if we don't specify what it should be reading

    fp = open(input, 'r') if iinput else sys.stdin
    out = out or print

    data_dict = dict()
    unparsed_rows = []
    line = fp.readline()
    while line:
        line = fp.readline()
        parsed_row = parse_row(line)
        if parsed_row is None:
            unparsed_rows.append(line)
            continue
        if parsed_row[0] not in data_dict:
            data_dict[parsed_row[0]] = {
                'id': parsed_row[0],
                'reviewer': []
            }
        row_dict = data_dict.get(parsed_row[0])
        row_dict.get('reviewer').append(
            {
                'id': parsed_row[1],
                'major_comments': parsed_row[2],
                'minor_comments': parsed_row[3],
                'competing_interests': parsed_row[4]
            }
        )

    [out(json.dumps(row)) for row in list(data_dict.values())]


if __name__ == '__main__':
    main()
