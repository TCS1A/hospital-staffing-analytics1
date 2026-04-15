import boto3
import pandas as pd
import time

athena = boto3.client('athena', region_name='us-east-1')
BUCKET = 'hospital-staffing-bucket'
DATABASE = 'hospital_staffing'

def run_athena_query(sql):
    response = athena.start_query_execution(
        QueryString=sql,
        QueryExecutionContext={'Database': DATABASE},
        ResultConfiguration={'OutputLocation': f's3://{BUCKET}/athena-results/'}
    )
    query_id = response['QueryExecutionId']

    # Wait for query to complete
    while True:
        status = athena.get_query_execution(QueryExecutionId=query_id)
        state = status['QueryExecution']['Status']['State']
        if state in ['SUCCEEDED', 'FAILED', 'CANCELLED']:
            break
        time.sleep(2)

    if state != 'SUCCEEDED':
        raise Exception(f'Query failed: {state}')

    # Get results
    results = athena.get_query_results(QueryExecutionId=query_id)
    rows = results['ResultSet']['Rows']
    headers = [col['VarCharValue'] for col in rows[0]['Data']]
    data = [[col.get('VarCharValue', '') for col in row['Data']] for row in rows[1:]]
    return pd.DataFrame(data, columns=headers)

# Metric 1 — Nurse-to-Patient Ratio by State
print('Running Metric 1...')
metric1 = run_athena_query("""
    SELECT STATE,
           ROUND(AVG(nurse_patient_ratio), 2) AS avg_ratio
    FROM staffing_gold
    GROUP BY STATE
    ORDER BY avg_ratio DESC
    LIMIT 10
""")
print(metric1.to_string(index=False))
metric1.to_csv('outputs/metric1_athena.csv', index=False)

# Metric 2 — Total Hours by State
print('\nRunning Metric 2...')
metric2 = run_athena_query("""
    SELECT STATE,
           ROUND(SUM(total_nurse_hrs), 0) AS total_hours
    FROM staffing_gold
    GROUP BY STATE
    ORDER BY total_hours DESC
    LIMIT 10
""")
print(metric2.to_string(index=False))
metric2.to_csv('outputs/metric2_athena.csv', index=False)

print('\n✅ Athena metrics complete!')