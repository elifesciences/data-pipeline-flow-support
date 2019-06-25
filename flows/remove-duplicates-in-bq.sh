#!/bin/bash
set -eu

project="$1"
dataset="$2"
table="$3"
unique_field="$4"
order_field="$5"


SQL="DELETE FROM \`{project}.{dataset}.{table}\` WHERE STRUCT({unique_field}, {order_field}) NOT IN (SELECT AS STRUCT {unique_field}, MAX({order_field})  FROM \`{project}.{dataset}.{table}\`  GROUP BY {unique_field})"
SQL=$(sed -e "s/{project}/"$project"/g" <<< $SQL)
SQL=$(sed -e "s/{dataset}/"$dataset"/g" <<< $SQL)
SQL=$(sed -e "s/{table}/"$table"/g" <<< $SQL)
SQL=$(sed -e "s/{unique_field}/"$unique_field"/g" <<< $SQL)
SQL=$(sed -e "s/{order_field}/"$order_field"/g" <<< $SQL)
SQL=$(sed -e "s/\`/\\\\\`/g" <<< $SQL)

sudo -u elife --login /bin/bash << EOF
bq query --nouse_legacy_sql "$SQL"
EOF
