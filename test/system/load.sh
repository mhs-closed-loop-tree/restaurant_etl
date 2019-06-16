source setup.sh
source ../../trap.sh

cd ../../

echo Copying test data to bucket
gsutil cp $OUT_FILENAME gs://$BUCKET_NAME

SQL_IP=`gcloud $QUIET sql instances describe $INSTANCE_NAME |fgrep ' ipAddress' | cut -c 14-30`

echo Truncating staging table...
psql -h $SQL_IP -U $DATABASE_USER_NAME -d $DATABASE_NAME < sql/truncate_staging.sql

echo Starting SQL Import to staging table...
gcloud sql import csv $INSTANCE_NAME gs://$BUCKET_NAME/$OUT_FILENAME --database=$DATABASE_NAME --table=$TABLE_NAME

cd -
