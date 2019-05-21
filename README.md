# data-pipeline flow support repository

This repository contains the scripts, tools and tests neccessary to support the NiFi flows in the 
[data-pipeline project](https://github.com/elifesciences/data-pipeline-formula).

It's important to note that changes to the code in this repository *do not* go through CI/CD (yet), and that the master
branch of this repository is cloned as-is into the `/opt/flow-support/` directory of the data-pipeline project. 
See the [project's formula](https://github.com/elifesciences/data-pipeline-formula) for more details.

This repository replaces `data-pipeline-ejp-csv-deposit`.

## ./flows

The `./flows` directory contains a description of each of the flows and any scripts (and their tests) required for that
flow to run.

Python and bash scripts are kept *very* simple as they must operate strictly on their inputs and without any context,
like a virtualenv or interactive shell.

More complex transformations happen within Docker containers and may live in a different repository. This will be noted 
in that flow's README.

## ./nifi-expression-language

NiFi uses a JVM scripting language called Groovy with their own library and calls it the 
[NiFi Expression Language](https://nifi.apache.org/docs/nifi-docs/html/expression-language-guide.html) (EL).

This language is used extensively within our flows but suffers from not being particularly easy to work with *outside*
of NiFi.

The directory `./nifi-expression-language` contains a small Groovy program called `testEL.groovy` that can be used to 
evaulate EL expressions, and scripts that demonstrate it's usage. For example:

    $ ./table-name.sh "ejp_query_tool_query_id_380_DataScience:_Early_Career_Researchers_2018_09_03_eLife.csv"
    => 380_datascience_early_career_researchers

These scripts are examples *only* and are not executed by processors within the flows at all.
