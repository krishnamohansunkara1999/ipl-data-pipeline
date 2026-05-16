import boto3
import os

BUCKET_NAME = "ipl-data-pipeline-krishna"
REGION = "us-east-1"

s3 = boto3.client("s3", region_name=REGION)

files = [
    "data/matches.csv",
    "data/deliveries.csv"
]

def upload_to_s3(local_path, bucket, s3_key):
    print(f"Uploading {local_path}...")
    s3.upload_file(local_path, bucket, s3_key)
    print(f"✓ Done → s3://{bucket}/{s3_key}")

for file in files:
    filename = os.path.basename(file)
    s3_key = f"raw/{filename}"
    upload_to_s3(file, BUCKET_NAME, s3_key)

print("\n All files uploaded to S3 successfully!")