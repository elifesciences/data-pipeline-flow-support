#!/bin/bash
curl "https://hypothes.is/api/search?group=imRGyeeV&limit=200&offset=400" | jq . > /tmp/response.json
cat /tmp/response.json | python -m src.hy2bq
