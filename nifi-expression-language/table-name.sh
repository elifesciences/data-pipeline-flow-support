#!/bin/bash
# converts a filename of the type uploaded by EJP to a table name used in BigQuery

# todo: turn these into tests
# examples of input:
# ejp_query_tool_query_id_380_DataScience:_Early_Career_Researchers_2018_09_03_eLife.csv
# ejp_query_tool_query_id_489_DataScience:_Editor_Keywords_2018_09_03_eLife.csv
# ejp_query_tool_query_id_455_DataScience:_Editors_2018_09_03_eLife.csv

set -eux
input=$1
groovy testEL.groovy \
    -D "filename=$input" \
    '${filename:substring(0, ${filename:length():minus(21)}):replaceFirst("ejp_query_tool_query_id_", ""):toLower():replace(":", ""):replace("_-_", "_")}'
