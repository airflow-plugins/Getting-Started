# Import Airflow specific dependencies.
from airflow import DAG
from airflow.operators import DummyOperator
from airflow.operators.python_operator import PythonOperator
from datetime import datetime

# Import the module for the FTP..
from ftplib import FTP


# Define functions
def upload_file(**kwargs):
    """
    Uploads file as binary to FTP.
    """

    credentials = kwargs.get('templates_dict').get('credentials', None)
    host = credentials['host']
    username = credentials['username']
    password = credentials['password']
    port = credentials['port']

    ftp = FTP(host)
    ftp.login(username, password, port)

    filename = 'test.csv'
    ftp.storbinary('STOR ' + filename, open(filename, 'rb'))
    ftp.quit()


def download_file(**kwargs):
    """
    Downloads file from FTP.
    """

    credentials = kwargs.get('templates_dict').get('credentials', None)
    host = credentials['host']
    username = credentials['username']
    password = credentials['password']

    ftp = FTP(host)
    ftp.login(username, password)

    filename = '/files/test_ah/sample_data.csv'

    localfile = open('test.csv', 'wb')
    print("HERE!")
    ftp.retrbinary('RETR ' + filename, localfile.write, 1024)

    ftp.quit()
    localfile.close()


default_args = {
    'owner': 'airflow',
    'start_date': datetime(2017, 12, 19)
}


# Schedule this DAG to run once.
dag = DAG('ah_ftp_python_ops',
          description='Manipulating FTPs with PythonOperators',
          schedule_interval='@once',
          start_date=datetime(2017, 12, 18),
          default_args=default_args)

# FTP creds
credentials = {
    'host': '',
    'username': '',
    'password': '',
    'port': 21

}
with dag:
    # Dummy start DAG.
    kick_off_dag = DummyOperator(task_id='kick_off_dag')

    # Call the functions

    download_file = PythonOperator(
        task_id='download_file',
        python_callable=download_file,
        # This passes the date into the function as a dictionaryt.
        templates_dict={'credentials': credentials},
        provide_context=True
    )

    upload_file = PythonOperator(
        task_id='upload_file',
        python_callable=upload_file,  # function-name
        # This passes the params into the function as a dictionaryt.
        templates_dict={'credentials': credentials},
        provide_context=True
    )

    # Set dependencies.
    # A task won't start until the one before it does.
    # e.g. the upload won't start until the download taks finishes.
    kick_off_dag >> download_file >> upload_file
