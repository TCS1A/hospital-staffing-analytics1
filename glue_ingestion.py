import boto3
import urllib.request
import os

# Google Drive direct download URL format
DRIVE_FILES = {
    'PBJ_Daily_Nurse_Staffing_Q2_2024.csv': 'YOUR_GOOGLE_DRIVE_FILE_ID',
    'Skilled_Nursing_Facility_Quality_Reporting_Program_National_Data_Oct2024.csv': 'YOUR_FILE_ID_2',
    'Skilled_Nursing_Facility_Quality_Reporting_Program_Provider_Data_Oct2024.csv': 'YOUR_FILE_ID_3',
    'Swing_Bed_SNF_data_Oct2024.csv': 'YOUR_FILE_ID_4',
}

BUCKET = 'hospital-staffing-bucket'
s3 = boto3.client('s3')

def get_drive_url(file_id):
    return f'https://drive.google.com/uc?export=download&id={file_id}'

def check_already_ingested(filename):
    key = f'raw/pbj_staffing/year=2024/quarter=Q2/{filename}'
    try:
        s3.head_object(Bucket=BUCKET, Key=key)
        return True
    except:
        return False

def upload_to_s3(local_path, s3_key):
    s3.upload_file(local_path, BUCKET, s3_key)
    print(f'✅ Uploaded: {s3_key}')

for filename, file_id in DRIVE_FILES.items():
    if check_already_ingested(filename):
        print(f'⏭️  Already ingested — skipping: {filename}')
        continue

    print(f'Downloading: {filename}')
    local_path = f'/tmp/{filename}'
    urllib.request.urlretrieve(get_drive_url(file_id), local_path)

    s3_key = f'raw/pbj_staffing/year=2024/quarter=Q2/{filename}'
    upload_to_s3(local_path, s3_key)
    os.remove(local_path)

print('✅ Ingestion job complete!')