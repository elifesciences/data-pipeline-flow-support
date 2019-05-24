# Manuscript reviews csv deposit flow

Consists of single script:

* `src/reviewercsv2bq.py`

and the BigQuery schema:

* `schema.json`

This is scripts in this project are used in the nifi data pipeline which monitors reviewers comments S3 buckets for new files, 
retrieves new new reviewer files , and passes the contents of the file as `stdin` for the python script
`reviewercsv2bq.py` which then processes the data and emits lines of json on `stdout`.

The cleansed, merged data is uploaded to the `elife-data-pipeline.$env.manuscript review` table in BigQuery.
