# ejp-csv-deposit

Consists of:

* scripts/ejpcsv2json.py
* scripts/load-file-to-bq.sh

and all of the BigQuery schemas in `./schemas`

This flow monitors the `elife-ejp-ftp` S3 bucket for the daily upload of SQL results dumps ('reports') from our provider
EJP.

Only specific reports in the bucket are parsed, the data is transformed from CSV to JSON, provenance information added
and the results uploaded to Google's BigQuery cloud service.

Results are uploaded to BigQuery in atomic units (rather than individual rows) with support for throttling when a large
number of reports are to be processed.

## how to add a new report

Occasionally new reports are added to EJP, or an old one is selected for inclusion, and it's processing must be 
integrated in to the flow and uploaded to BigQuery.

At time of writing we have three reports sharing their BQ table with another report. If the report you're adding shares
the table of another extant table, skip to step #4.

To add a new report:

1. generate the BigQuery table name from the report name

for example, this:

    > ejp_query_tool_query_id_779_DataScience:_Reviewer_info_-_all_2018_12_05_eLife.csv
    
becomes

    > 779_datascience_reviewer_info_all
    
using the [table-name.sh](../../nifi-expression-language/table-name.sh) script.

2. create a table in BigQuery

It should live alongside all the other report tables with this naming convention.

It's fields should consist of the headers from the report as well as:

* `date_generated` (DATE type) 
* `imported_timestamp` (TIMESTAMP type)
* `provenance` (RECORD type) with sub-records:
    - `source_filename` (STRING type)

See the schema files of existing reports. This JSON can be copied+pasted into BQ - **do not** waste your time adding 
fields and fiddling with types. Mistakes in the schema cannot be easily altered in BQ, just destroy the table and paste
the schema into a new table.

3. add reports of this new type to the [FilterByReportName](https://prod--pipeline.elifesciences.org/nifi/?processGroupId=46923093-852a-1d2e-149a-36cc00737ad5&componentIds=852a1d30-3073-1692-0db4-d4ecc2bfa03a) NiFi processor.

This adds the new report to a whitelist of supported reports.

Under properties you will see a list of already defined reports (the processor must be in the 'stopped' state to 
modify it).

The `Property` key isn't important, it's only used as the relationship name, but the `Value` is a NiFi expression 
language predicate similar to:

    > ${filename:startsWith("ejp_query_tool_query_id_779_DataScience:_Reviewer_info_-_all_")}

The code should be self explanatory to any programmer, just remember to *exclude the trailing timestamp*.

4. handle shared tables 

At time of writing we have three reports sharing their BQ table with another report. If the report you're adding shares
the table of another then the new report *must change the value of the automatically generated table name* for that 
report.

Under 'Advanced' in the `HandleSharedTables` processor's properties, add a new rule following the examples already there 
and ensure the 'Attribute' under the `Actions` field is `bigquery_table` and the value is the name of the pre-existing
table.

5. test the new support by uploading a report to the 'fixed' bucket

The ejp-csv-deposit pipeline monitors two buckets for content, the one EJP uploads reports to and another called 
`ListFixedFiles` where adhoc reports can be uploaded to. These are typically reports that failed the first time through
and need to be inspected and fixed before going through again.

Testing should be done on the *staging* flow and never in the production flows.

