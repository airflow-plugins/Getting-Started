from airflow import DAG
from airflow.operators import DummyOperator
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
from airflow.contrib.hooks import FTPHook


def upload_file(**kwargs):
    """
    Uploads file as binary to FTP.
    """

    hook = FTPHook(ftp_conn_id='astro_ftp').get_conn()

    local_path = 'sample_data.csv'
    remote_path = '/files/test_ah/sample_data.csv'

    hook.store_file(local_path, remote_path)
    hook.close_conn()


def download_file(**kwargs):
    """
    Downloads file from FTP.
    """
    hook = FTPHook(ftp_conn_id='astro_ftp')

    local_path = 'sample_data.csv'
    remote_path = '/files/test_ah/sample_data.csv'

    hook.retrieve_file(remote_path, local_path)
    hook.close_conn()


default_args = {
    'owner': 'airflow',
    'start_date': datetime(2017, 12, 19)
}


# Schedule this DAG to run once.
dag = DAG('ah_ftp_hook',
          description='Manipulating FTPs with PythonOperators+Hooks',
          schedule_interval='@once',
          start_date=datetime(2017, 12, 18),
          default_args=default_args)

with dag:

    kick_off_dag = DummyOperator(task_id='kick_off_dag')

    upload_file = PythonOperator(
        task_id='upload_file',
        python_callable=upload_file,
        # This passes the params into the function.
        provide_context=True
    )

    download_file = PythonOperator(
        task_id='download_file',
        python_callable=download_file,
        # This passes the date into the function.
        provide_context=True
    )

    # Set dependencies.
    kick_off_dag >> download_file >> upload_file
