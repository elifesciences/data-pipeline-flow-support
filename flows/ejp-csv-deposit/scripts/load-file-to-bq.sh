#!/bin/bash
set -eu

location="$1"
dataset="$2"
table="$3"
path_to_source="$4"

sudo -u elife --login /bin/bash << EOF
bq --location="$location" load \
    --headless \
    --source_format=NEWLINE_DELIMITED_JSON \
    "$dataset.$table" \
    "$path_to_source"
EOF
