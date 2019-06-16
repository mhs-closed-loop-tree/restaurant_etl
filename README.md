# restaurant_etl
Contain the code related to the Restaurant ETL process

Core features include:

(1) Automated fetch from source
(2) Transformation and validation against a well defined schema
(3) Loading to staging table
(4) Verification of overall load state (expected row count threshold)
(5) Aggregation into the main search table
(6) Lineage metadata including source data row, and load timestamp
(7) Good error handling practices

**Please note for each restaurant the entry is based upon the latest grading date entry for each restaurant.**

# Instructions

Please see the restaurant_db repo for environment setup instructions

In order to run the load procedure execute **load.sh** from the command line. The script includes environment specific configuration properties which would normally come from CI.

The process assumes that the executing shell has Google Cloud authorisation. Normally we'd use a shared or load-specific service account key to auth.

