# Import Airflow specific dependencies.
from airflow import DAG
from airflow.operators import DummyOperator
from plugins.ftp_plugin.operators.ftp_to_s3_operator import FTPToS3Operator
from datetime import datetime

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2017, 12, 19)
}

# Schedule this DAG to run once.
dag = DAG('ah_ftp_full',
          description='FTPs with FTPOperator',
          schedule_interval='@once',
          start_date=datetime(2017, 12, 18),
          default_args=default_args)

files = [
    {
        'name': 'sample_one.csv',
        'delete': True,
    },

    {
        'name': 'sample_two.csv',
        'delete': False
    },

    {
        'name': 'sample_three.csv',
        'delete': True

    }
]

with dag:
    # Dummy start DAG.
    kick_off_dag = DummyOperator(task_id='kick_off_dag')
    for file in files:
        ftp_to_s3 = FTPToS3Operator(
            task_id='download_file_{0}'.format(file['name']),
            ftp_conn_id='astro-ftp',
            ftp_director='/files/test_ah/sample_data.csv',
            local_path='/temp/{0}'.format(file['name']),
            s3_conn_id='astronomer-s3	',
            s3_bucket='astronomer-worflows-dev',
            s3_key=file['name'],
            delete=file['delete']
        )

        kick_off_dag >> ftp_to_s3
