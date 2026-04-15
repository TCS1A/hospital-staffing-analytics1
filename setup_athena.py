import boto3

athena = boto3.client('athena', region_name='us-east-1')
BUCKET = 'hospital-staffing-bucket'

# Create Athena database
athena.start_query_execution(
    QueryString='CREATE DATABASE IF NOT EXISTS hospital_staffing',
    ResultConfiguration={'OutputLocation': f's3://{BUCKET}/athena-results/'}
)
print('✅ Database created')

# Register Delta Lake table in Athena
create_table = """
CREATE EXTERNAL TABLE IF NOT EXISTS hospital_staffing.staffing_gold (
    PROVNUM     string,
    PROVNAME    string,
    CITY        string,
    STATE       string,
    COUNTY_NAME string,
    WorkDate    bigint,
    MDScensus   double,
    Hrs_RN      double,
    Hrs_LPN     double,
    Hrs_CNA     double,
    total_nurse_hrs    double,
    nurse_patient_ratio double,
    emp_hrs_total      double,
    ctr_hrs_total      double
)
LOCATION 's3://hospital-staffing-bucket/gold/staffing/'
TBLPROPERTIES ('table_type'='DELTA');
"""

athena.start_query_execution(
    QueryString=create_table,
    QueryExecutionContext={'Database': 'hospital_staffing'},
    ResultConfiguration={'OutputLocation': f's3://{BUCKET}/athena-results/'}
)
print('✅ Delta Lake table registered in Athena')
print('You can now query it in Athena console or connect QuickSight')