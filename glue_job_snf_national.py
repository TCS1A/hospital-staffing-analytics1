import sys
from awsglue.context import GlueContext
from pyspark.context import SparkContext

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

BUCKET = 'hospital-staffing-bucket'
RAW_PATH = f's3://{BUCKET}/raw/supporting/snf_quality/year=2024/Skilled_Nursing_Facility_Quality_Reporting_Program_National_Data_Oct2024.csv'
SILVER_PATH = f's3://{BUCKET}/processed/snf_national/'

print('JOB 2 — SNF National: Reading raw data...')
df = spark.read \
    .option('header', 'true') \
    .option('inferSchema', 'true') \
    .option('charset', 'ISO-8859-1') \
    .csv(RAW_PATH)

print(f'Rows loaded: {df.count()}')
df_clean = df.dropna()
df_clean.write.mode('overwrite').parquet(SILVER_PATH)
print('JOB 2 — SNF National: Complete')