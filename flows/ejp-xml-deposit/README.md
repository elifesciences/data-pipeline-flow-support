# ejp-xml-deposit

Consists of:

* the Python application [data-pipeline-ejp-to-json-convertor](https://github.com/elifesciences/data-pipeline-ejp-to-json-converter)
* that executes within a Docker container
* storing state within a PostgreSQL sidecar container
* before being pushed to BigQuery with a [custom script](https://github.com/elifesciences/data-pipeline-ejp-to-json-converter/blob/develop/update-big-query.sh)

as well as supporting scripts:

* [process-zip-apply.sh](https://github.com/elifesciences/data-pipeline-formula/blob/master/salt/data-pipeline/scripts/process-zip-apply.sh)
* [update-big-query-wrapper.sh](https://github.com/elifesciences/data-pipeline-formula/blob/master/salt/data-pipeline/scripts/update-big-query-wrapper.sh)

The `ejp-xml-deposit` flow monitors the S3 bucket `elife-ejp-ftp-db-xml-dump` for the daily upload of the partial 
database dump from EJP. The dump includes everything that has been updated in the last day and requires substantial 
processing before the results are eventually flushed to BigQuery.

The processing occurs in the `ProcessXMLZipFilename` processor after the dump has been downloaded and unzipped. This
processor calls the `process-zip-apply.sh` script that invokes `ejp-to-json-convertor` within the Docker container.

On success it generates a 'signal', a flow file that accumulates with other 'signals' until a set of conditions are 
reached and a single empty flow file is emitted that triggers flushing the results to BigQuery.

This batching-before-flushing behaviour is because the `ejp-to-json-convertor` script can handle the processing of many
database dumps before the results should be flushed to BQ. The typical usecase is processing the daily dump, but 
processing many dumps as quickly as possible is also supported.

## history

`ejp-xml-deposit` and `ejp-csv-deposit` were the two flows first created and both have undergone substantial changes 
since as we handle the data, learn more about NiFi and get a feeling for where these scripts should live. Right now 
the support scripts are living in the `data-pipeline` formula (the description of how the project is configured) but 
may be shifted into this repository.
