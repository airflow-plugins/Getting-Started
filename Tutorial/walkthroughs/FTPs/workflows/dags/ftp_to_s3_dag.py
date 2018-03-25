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
dag = DAG('ah_ftp_operator',
          description='FTPs with FTPOperator',
          schedule_interval='@once',
          start_date=datetime(2017, 12, 18),
          default_args=default_args)


with dag:
    # Dummy start DAG.
    kick_off_dag = DummyOperator(task_id='kick_off_dag')

    # Call the functions

    ftp_to_s3 = FTPToS3Operator(
        task_id='download_file',
        ftp_conn_id='astro_ftp',
        ftp_directory='/files/test_ah/sample_data.csv',
        local_path='test_data.csv',
        s3_conn_id='astronomer-s3',
        s3_bucket='astronomer-worflows-dev',
        s3_key='test_data.csv',
    )

    # A task won't start until the one before it does.
    # e.g. the upload won't start until the download taks finishes.
    kick_off_dag >> ftp_to_s3
