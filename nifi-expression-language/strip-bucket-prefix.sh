#!/bin/bash
set -eux
input="$1"
groovy testEL.groovy \
    -D "filename=$input" \
    '${filename:substringAfterLast("/")}'
