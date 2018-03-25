from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from plugins.google_analytics_plugin.operators.google_analytics_reporting_to_s3_operator import GoogleAnalyticsReportingToS3Operator


s3_bucket = 'astronomer-workflows-dev'
s3_conn_id = 'astronomer-s3'

time_string = '{{ ts_nodash }}'
google_analytics_conn_id = 'google_analytics_connection'

execution_date = '{{ execution_date }}'
next_execution_date = '{{ next_execution_date }}'


view_id = ''

end_date = datetime.today()
start_date = end_date - timedelta(days=6)

pipelines = [
    {
        'name': 'demographics',
        'dimensions': [
            {'name': 'ga:date'},
            {'name': 'ga:userAgeBracket'},
            {'name': 'ga:userGender'}
        ],
        'metrics': [
            {'expression': 'ga:sessions'}
        ],

        # TODO: Destination schema.
        'schema': [
            {}
        ]
    },

    {
        'name': 'date_sessions',
        'dimensions': [
            {'name': 'ga:date'},
        ],
        'metrics': [
            {'expression': 'ga:sessions'}
        ],

        # TODO: Destination schema.
        'schema': [
            {}
        ]
    },
    {
        'name': 'medium_source',
        'dimensions': [
            {'name': 'ga:medium'},
            {'name': 'ga:source'},
        ],
        'metrics': [
            {'expression': 'ga:sessions'},
            {'expression': 'ga:avgTimeOnPage'},
            {'expression': 'ga:avgTimeOnPage'},
        ],

        # TODO: Destination schema.
        'schema': [
            {}
        ]
    },
]

default_args = {


    'start_date': datetime(2018, 3, 20, 0, 0),
    'email': ['l5t3o4a9m9q9v1w9@astronomerteam.slack.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 0,
}

dag = DAG(
    'core_reporting_test',
    schedule_interval='@daily',
    default_args=default_args,
    catchup=True
)

with dag:

    start = DummyOperator(task_id='start')



    for pipeline in pipelines:
        google_analytics = GoogleAnalyticsReportingToS3Operator(
            task_id='ga_reporting_{endpoint}_to_s3'.format(
                endpoint=pipeline['name']),
            google_analytics_conn_id=google_analytics_conn_id,
            view_id=view_id,
            since=execution_date,
            until=next_execution_date,
            sampling_level='LARGE',
            dimensions=pipeline['dimensions'],
            metrics=pipeline['metrics'],
            page_size=100,
            include_empty_rows=True,
            s3_conn_id=s3_conn_id,
            s3_bucket=s3_bucket,
            s3_key='ga_reporting_{endpoint}_{time_string}'.format(
                endpoint=pipeline['name'], time_string=time_string)
        )


        start >> google_analytics
