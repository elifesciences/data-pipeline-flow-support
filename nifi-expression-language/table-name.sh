#!/bin/bash
set -eux
input=$1
groovy testEL.groovy \
    -D "filename=$input" \
    '${filename:substring(0, ${filename:length():minus(21)}):replaceFirst("ejp_query_tool_query_id_", ""):toLower():replace(":", ""):replace("_-_", "_")}'
