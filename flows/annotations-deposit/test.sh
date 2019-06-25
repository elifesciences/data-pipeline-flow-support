#!/bin/bash
curl "https://hypothes.is/api/search?group=imRGyeeV&limit=200&offset=400" | jq . > /tmp/response.json
cat /tmp/response.json | python -m src.hy2bq "2016-09-17T03:24:21.634919+00:00"
