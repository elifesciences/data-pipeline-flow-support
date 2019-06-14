# People and Profile api deposit flow

Consists of single script:

* `src/people_profile_json_download.py`

and the BigQuery schemas:

* `schema/people_orcid_profile_schema.json` for the profile's table
* `schema/people_staff_profile_schema.json` for the people's table

This is scripts in this project are used in the nifi data pipeline which daily/weekly downloads the full data from people and profile api,
using the python script `people_profile_json_download.py` which then processes the data and emits lines of json on `stdout`. 
Emmitted data is then uploaded into the big query table `elife-data-pipeline.$env.people_orcid_profile` and `elife-data-pipeline.$env.people_staff_profile`
for the profile and people api respectively  