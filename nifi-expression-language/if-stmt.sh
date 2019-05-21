#!/bin/bash
# returns different bucket names depending on the given environment
# ./if-stmt.sh prod => "elife-ejp-ftp"
# ./if-stmt.sh staging => "elife-ejp-ftp--staging"

set -eu
input=$1
groovy testEL.groovy \
    -D "env=$input" \
    '${env:equals("prod"):ifElse("elife-ejp-ftp", ${literal("elife-ejp-ftp--"):append(${env})})}'
