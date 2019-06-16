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

echo Preparing and Validating the data...
python src/pre_process.py $IN_FILENAME $OUT_FILENAME


