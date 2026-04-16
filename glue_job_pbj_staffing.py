import sys
from awsglue.context import GlueContext
from pyspark.context import SparkContext
from pyspark.sql import functions as F

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

BUCKET = 'hospital-staffing-bucket'
RAW_PATH = f's3://{BUCKET}/raw/pbj_staffing/year=2024/quarter=Q2/'
SILVER_PATH = f's3://{BUCKET}/processed/pbj_staffing/'

print('JOB 1 — PBJ Staffing: Reading raw data...')
df = spark.read \
    .option('header', 'true') \
    .option('inferSchema', 'true') \
    .option('charset', 'ISO-8859-1') \
    .csv(RAW_PATH)

print(f'Rows loaded: {df.count()}')
df_clean = df.dropna(subset=['PROVNUM', 'WorkDate', 'MDScensus'])
df_clean = df_clean \
    .withColumn('total_nurse_hrs', F.col('Hrs_RN') + F.col('Hrs_LPN') + F.col('Hrs_CNA')) \
    .withColumn('nurse_patient_ratio', F.col('total_nurse_hrs') / F.when(F.col('MDScensus') > 0, F.col('MDScensus'))) \
    .withColumn('emp_hrs_total', F.col('Hrs_RN_emp') + F.col('Hrs_LPN_emp') + F.col('Hrs_CNA_emp')) \
    .withColumn('ctr_hrs_total', F.col('Hrs_RN_ctr') + F.col('Hrs_LPN_ctr') + F.col('Hrs_CNA_ctr'))

df_clean.write.mode('overwrite').parquet(SILVER_PATH)
print('JOB 1 — PBJ Staffing: Complete')