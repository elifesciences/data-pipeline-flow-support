# annotations deposit flow

Consists of two scripts:

* `src/hy2bq.py`
* `queryuntil.sh`

The script `queryuntil.sh` queries Hypothesis until there are no more results, sending all results to the python script
`hy2bq.py` that processes the response data and emits lines of json on `stdout`.

These lines of json are captured by NiFi and uploaded to the `elife-data-pipeline.$env.annotations` table in BigQuery.

The `queryuntil.sh` script maintains an environment-specific state file containing the last date it's seen from the 
results. This date value is used when requesting the next page of results.

At time of writing (2019-04-18) there is a bug in the Hypothesis API that disregards the time component of the date 
value we maintain for use in the `search_after` URL parameter. For example, queries for annotations made 
"in the last hour" will return all of the results for that day.
