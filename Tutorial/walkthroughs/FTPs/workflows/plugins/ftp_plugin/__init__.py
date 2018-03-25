from airflow.plugins_manager import AirflowPlugin
from ftp_plugin.operators.ftp_to_s3_operator import FTPToS3Operator


class SFTPToS3Plugin(AirflowPlugin):
    name = "FTPToS3Operator"
    operators = [FTPToS3Operator]
    hooks = []
    executors = []
    macros = []
    admin_views = []
    flask_blueprints = []
    menu_links = []
