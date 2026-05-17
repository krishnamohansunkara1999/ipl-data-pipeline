from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from datetime import datetime
import boto3
import pandas as pd
from io import StringIO

default_args = {
    'owner': 'krishna',
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
}

dag = DAG(
    'ipl_pipeline',
    default_args=default_args,
    schedule='@daily',
    catchup=False,
)

def upload_to_s3():
    s3 = boto3.client('s3', region_name='us-east-1')
    files = ['matches.csv', 'deliveries.csv']
    for file in files:
        s3.upload_file(f'/home/ubuntu/{file}', 'ipl-data-pipeline-krishna', f'raw/{file}')
    print("Upload complete!")

def transform_data():
    s3 = boto3.client('s3', region_name='us-east-1')
    obj = s3.get_object(Bucket='ipl-data-pipeline-krishna', Key='raw/matches.csv')
    df = pd.read_csv(obj['Body'])
    df = df.dropna(subset=['winner', 'team1', 'team2'])
    win_counts = df.groupby('winner').size().reset_index(name='total_wins')
    win_counts = win_counts.sort_values('total_wins', ascending=False)
    csv_buffer = StringIO()
    win_counts.to_csv(csv_buffer, index=False)
    s3.put_object(Bucket='ipl-data-pipeline-krishna', Key='refined/matches_refined.csv', Body=csv_buffer.getvalue())
    print("Transform complete!")

upload_task = PythonOperator(
    task_id='upload_to_s3',
    python_callable=upload_to_s3,
    dag=dag,
)

transform_task = PythonOperator(
    task_id='transform_data',
    python_callable=transform_data,
    dag=dag,
)

upload_task >> transform_task