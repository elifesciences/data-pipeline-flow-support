#!/bin/bash
# intended to be run periodically (every minute, hour, day, etc)
# stores date of last updated record in file '<env>-statefile'
# runs until there are fewer than results per-page in resultset

set -eu

environment=$1
statefile="$environment-state"
outfile=$(mktemp)

touch "$statefile"

#search_after="2012-06-20T23:14:23.000000+00:00" # earliest record
default_search_after="2012-01-01T01:01:01.000000+00:00"
search_after=$(cat "$statefile")
if [ -z "$search_after" ]; then search_after="$default_search_after"; fi
results_per_page=200 # 200 is max

while true; do
    # the date of the last record has to be extracted and used in the next request
    > "$outfile" curl --silent "https://hypothes.is/api/search?group=imRGyeeV&sort=updated&order=asc&limit=$results_per_page&search_after=$search_after"

    # NOTE: `search_after` parameter does not consider the time component of the query
    # the python script does further comparison of dates

    # WARN: what are the effects if there are more than 200 results in a day?
    # this script wouldn't halt for example. with 201 results in a single day:
    # * the request would be made
    # * 200 results returned
    # * the 200th timestamp would be recorded and used as input into the next request
    # * loop recurs
    # * request is made but time component ignored
    # * 200 results returned ...

    # emit processed results to be handled by nifi
    cat "$outfile" | python3 -m src.hy2bq "$search_after"

    # capture a pointer for later calls to script
    search_after=$(cat "$outfile" | jq '(.rows[])' -c | tail -n 1 | jq -r '.updated')
    echo "$search_after" > "$statefile"

    # figure out if we need to recur
    row_count=$(cat "$outfile" | jq '.rows | length')
    if [ "$row_count" -lt "$results_per_page" ]; then
        break # nothing left to scrape
    fi

    # recur. uses date from last request in new request, advancing pointer through remote resultset
done

rm -f "$outfile"
