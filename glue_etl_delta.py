import sys
from awsglue.context import GlueContext
from pyspark.context import SparkContext
from pyspark.sql import functions as F
from delta.tables import DeltaTable

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

# Enable Delta Lake
spark.conf.set("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
spark.conf.set("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")

BUCKET = 'hospital-staffing-bucket'
RAW_PATH = f's3://{BUCKET}/raw/pbj_staffing/year=2024/quarter=Q2/'
GOLD_PATH = f's3://{BUCKET}/gold/staffing/'

print('Reading raw data from S3...')
df_new = spark.read \
    .option('header', 'true') \
    .option('inferSchema', 'true') \
    .option('charset', 'ISO-8859-1') \
    .csv(RAW_PATH)

# Clean and derive columns
df_new = df_new.dropna(subset=['PROVNUM', 'WorkDate', 'MDScensus'])

df_new = df_new \
    .withColumn('total_nurse_hrs', F.col('Hrs_RN') + F.col('Hrs_LPN') + F.col('Hrs_CNA')) \
    .withColumn('nurse_patient_ratio', F.col('total_nurse_hrs') / F.when(F.col('MDScensus') > 0, F.col('MDScensus'))) \
    .withColumn('emp_hrs_total', F.col('Hrs_RN_emp') + F.col('Hrs_LPN_emp') + F.col('Hrs_CNA_emp')) \
    .withColumn('ctr_hrs_total', F.col('Hrs_RN_ctr') + F.col('Hrs_LPN_ctr') + F.col('Hrs_CNA_ctr'))

# Check if Delta table already exists
if DeltaTable.isDeltaTable(spark, GOLD_PATH):
    print('Delta table exists — running incremental MERGE...')
    delta_table = DeltaTable.forPath(spark, GOLD_PATH)

    # MERGE: update existing rows, insert new ones
    delta_table.alias('existing').merge(
        df_new.alias('new'),
        'existing.PROVNUM = new.PROVNUM AND existing.WorkDate = new.WorkDate'
    ).whenMatchedUpdateAll() \
     .whenNotMatchedInsertAll() \
     .execute()

    print('MERGE complete — incremental update done')
else:
    print('No Delta table found — writing full initial load...')
    df_new.write \
        .format('delta') \
        .mode('overwrite') \
        .save(GOLD_PATH)
    print('Initial Delta Lake table created')

print('✅ Glue Delta ETL job complete!')