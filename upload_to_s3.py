import boto3

s3 = boto3.client('s3')
BUCKET = 'hospital-staffing-bucket'  # ← change this to your actual bucket name

# Upload master file
s3.upload_file(
    Filename='data/PBJ_Daily_Nurse_Staffing_Q2_2024.csv',
    Bucket=BUCKET,
    Key='raw/pbj_staffing/year=2024/quarter=Q2/PBJ_Daily_Nurse_Staffing_Q2_2024.csv'
)
print('✅ Master file uploaded')

# Upload supporting files
supporting = [
    'Skilled_Nursing_Facility_Quality_Reporting_Program_National_Data_Oct2024.csv',
    'Skilled_Nursing_Facility_Quality_Reporting_Program_Provider_Data_Oct2024.csv',
    'Swing_Bed_SNF_data_Oct2024.csv'
]

for filename in supporting:
    s3.upload_file(
        Filename=f'data/supporting/{filename}',
        Bucket=BUCKET,
        Key=f'raw/supporting/snf_quality/year=2024/{filename}'
    )
    print(f'✅ Uploaded: {filename}')

print('\n🎉 All files uploaded to S3!')