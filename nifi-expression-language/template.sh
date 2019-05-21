#!/bin/bash
# given two input (stdout and stderr ostensibly), generates a JSON wrapper and ensures contents are properly escaped

#set -e # messes with `read`
set -ux

template='{"stderr": "{token1}", "stdout": "{token2}"}'
IFS='' read -r -d '' expr <<"EOF"
${
literal('{"stderr": "{token1}", "stdout": "{token2}"}')
    :replace("{token1}", ${execution.error:escapeJson()}) 
    :replace("{token2}", ${execution.stdout:escapeJson()})
}
EOF

groovy testEL.groovy -D "execution.stdout=$1" -D "execution.error=$2" "$expr"
