#!/bin/bash
set -e

function dump {
    project="elife-data-pipeline"
    dataset="nifidemo4_temp"
    table=$1
    echo "$table"
    # regarding --disable_ssl_validation
    # https://issuetracker.google.com/issues/117948931
    bq show --format prettyjson --disable_ssl_validation --schema "$project:$dataset.$table" > ./schemas/$table.json
}

dump 380_datascience_early_career_researchers
dump 455_datascience_editors
dump 489_datascience_editor_keywords
# reports 705 and 728 both go to the same table
dump 705_datascience_reviewer_identity_revealed_last_week
dump 767_datascience_person_roles
# reports 779 and 780 both go to the same table
dump 779_datascience_reviewer_info_all
# reports 795 and 796 both go to the same table
dump 795_datascience_person_merge_info_all
dump 1119_datascience_manuscript_reviews