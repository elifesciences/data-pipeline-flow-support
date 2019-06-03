# eLife Sciences Editors Google Spreadsheet Deposit Flow

Consists of single script:

* `src/editorscsv2json.py`

and the BigQuery schema:

* `schema.json`

This script in this project is used in the nifi data pipeline which retrieves eLife Sciences editors publicly available from  google spreadsheets, 
divides it into sheets, and passes the contents of each sheet as `stdin` for the python script
`editorscsv2json.py` which then processes the data and emits lines of json on `stdout`.

The data is uploaded to the `elife-data-pipeline.$env.public_editors_info` table in BigQuery.