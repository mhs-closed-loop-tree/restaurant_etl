# Handes the end to end load sequence, fetch, transform, validate, load, and SQL transform
# Requirements:  psql 		(including ~/.pgpass)
#                gcloud sdk

source trap.sh

python3 -m venv venv

source venv/bin/activate

pip install -r requirements.txt

# Note: set to '-q' to hide the step output and interactive prompts
QUIET=

LOAD_DATE=`date +%Y%m%d`
IN_FILENAME=restaurant.in.$LOAD_DATE.csv
OUT_FILENAME=restaurant.out.$LOAD_DATE.csv

BUCKET_NAME=tree-20190615
TABLE_NAME=restaurant__staging
DATABASE_NAME=tree
DATABASE_USER_NAME=tree
INSTANCE_NAME=tree



echo Fetching data file...
curl https://data.cityofnewyork.us/api/views/43nn-pn8j/rows.csv?accessType=DOWNLOAD -o$IN_FILENAME
# Handes the end to end load sequence, fetch, transform, validate, load, and SQL transform
# Requirements:  psql 		(including ~/.pgpass)
#                gcloud sdk

source trap.sh

python3 -m venv venv

source venv/bin/activate

pip install -r requirements.txt

# Note: set to '-q' to hide the step output and interactive prompts
QUIET=

LOAD_DATE=`date +%Y%m%d`
IN_FILENAME=restaurant.in.$LOAD_DATE.csv
OUT_FILENAME=restaurant.out.$LOAD_DATE.csv

BUCKET_NAME=tree-20190615
TABLE_NAME=restaurant__staging
DATABASE_NAME=tree
DATABASE_USER_NAME=tree
INSTANCE_NAME=tree



echo Fetching data file...
#curl https://data.cityofnewyork.us/api/views/43nn-pn8j/rows.csv?accessType=DOWNLOAD -o$IN_FILENAME

echo Preparing and Validating the data...
python src/pre_process.py $IN_FILENAME $OUT_FILENAME

echo Copying load file to GCS...
gsutil $QUIET cp $OUT_FILENAME gs://$BUCKET_NAME

SQL_IP=`gcloud $QUIET sql instances describe $INSTANCE_NAME |fgrep ' ipAddress' | cut -c 14-30`

echo Truncating staging table...
psql -h $SQL_IP -U $DATABASE_USER_NAME -d $DATABASE_NAME < sql/truncate_staging.sql

echo Starting SQL Import to staging table...
gcloud $QUIET sql import csv $INSTANCE_NAME gs://$BUCKET_NAME/$OUT_FILENAME --database=$DATABASE_NAME --table=$TABLE_NAME



