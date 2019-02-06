# data-pipeline-ejp-csv-deposit

This is the support repository for the `ejp-csv-deposit` 'flow' in the elife NiFi instance.

It contains scripts and documentation used by the flow and the `master` branch is found on the NiFi instance at `/opt/flows/ejp-csv-deposit`. This is where several processors reference scripts.

## ejp-csv-deposit

This flow monitors the `elife-ejp-ftp` S3 bucket for the daily upload of SQL results dumps ('reports') from our provider EJP.

Certain reports are filtered out, their data is transformed from CSV to JSON and the results uploaded to Google's BigQuery cloud service.

## adding a new report 

To add a new report to be processed and uploaded to BigQuery:

1. generate the BigQuery table name from the report name

for example, this:

    > ejp_query_tool_query_id_779_DataScience:_Reviewer_info_-_all_2018_12_05_eLife.csv
    
becomes

    > 779_datascience_reviewer_info_all
    
using the [table-name.sh](./scripts/table-name.sh) script (requires [Groovy](http://www.groovy-lang.org/)).

2. create a table in BigQuery 

It should live alongside all the other report tables with this naming convention.

It's fields should consist of the headers from the report as well as:

* `date_generated` (DATE type) 
* `imported_timestamp` (TIMESTAMP type)
* `provenance` (RECORD type) with sub-records:
    - `source_filename` (STRING type)

3. add reports of this new type to the `FilterByReportName` processor.

This adds the new report to a whitelist of supported reports.

Under properties you will see a list of already defined reports (the processor must be in the 'stopped' state to modify it).

The `Property` key isn't important, it's only used as the relationship name, but the `Value` is a NiFi expression language value similar to:

    > ${filename:startsWith("ejp_query_tool_query_id_779_DataScience:_Reviewer_info_-_all_")}

The code should be self explanatory to any programmer, just remember to *exclude the trailing timestamp*.

4. add report to the `RouteOnAttribute` processor 

At time of writing, the BigQuery processor we're using is a third party one and doesn't support dynamic table names. This means we need a very-similar-but-different processor for each table until first-class support is introduced to NiFi (it's on it's way).

Just like step 3, the `Property` key isn't that important, it just specifies the relationship name, but the `Value` this time is matching on the name of the table that was extracted from the `filename` attribute and added to the flowfile as a new attribute. This is the same name generated in step 1.

5. copy and paste an existing `PutBigQuery` processor

The name of the processor should be tweaked to match the report it's sending to BigQuery and the property `Bigquery Table` must be updated as well.

6. test the new support by uploading a report to the dummy bucket

The ejp-csv-deposit pipeline monitors two buckets for content, the one EJP uploads reports to and a dummy one where adhoc files can be uploaded to.

This works well for new tables but may interfere with tables already populated with data.




