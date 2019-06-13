#!/bin/bash
# converts a filename of the type uploaded by EJP to a table name used in BigQuery

set -e

function table_name {
    input="$1"
    printf "$input => "
    # stderr redirection is to hide the "Picked up _JAVA_OPTIONS ..." message
    2>/dev/null groovy testEL.groovy \
        -D "filename=$input" \
        '${filename:substring(0, ${filename:length():minus(21)}):replaceFirst("ejp_query_tool_query_id_", ""):toLower():replace(":", ""):replace("_-_", "_")}'
}

if [ -n "$1" ]; then
    table_name "$1"
else
    echo "old-style EJP filenames"

    table_name "ejp_query_tool_query_id_380_DataScience:_Early_Career_Researchers_2018_09_03_eLife.csv"
    table_name "ejp_query_tool_query_id_489_DataScience:_Editor_Keywords_2018_09_03_eLife.csv"
    table_name "ejp_query_tool_query_id_455_DataScience:_Editors_2018_09_03_eLife.csv"

    echo
    echo "new-style EJP filenames"

    table_name "ejp_query_tool_query_id_DataScience:_Early_Career_Researchers_2018_09_03_eLife.csv"
    table_name "ejp_query_tool_query_id_DataScience:_Editor_Keywords_2018_09_03_eLife.csv"
    table_name "ejp_query_tool_query_id_DataScience:_Editors_2018_09_03_eLife.csv"
fi
