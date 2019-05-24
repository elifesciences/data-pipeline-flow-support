# Manuscript reviewers csv deposit flow

Consists of two scripts:

* `src/reviewercsv2bq.py`
* `queryuntil.sh`

and the BigQuery schema:

* `schema.json`

This is scripts in this project are used in the nifi data pipeline which monitors reviewers comments S3 buckets for new files, 
retrieves new new reviewer files , and passes the contents of the file as stdin for the python script
`reviewercsv2bq.py` which then processes the data and emits lines of json on `stdout`.

These lines of json are captured by NiFi and uploaded to the `elife-data-pipeline.$env.manuscript review` table in BigQuery.


