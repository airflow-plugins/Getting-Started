from airflow.models import BaseOperator
from airflow.hooks.S3_hook import S3Hook
from airflow.contrib.hooks import FTPHook
import logging


class FTPToS3Operator(BaseOperator):
    """
    SFTP To S3 Operator
    :param ftp_conn_id:     The source FTP conn_id.
    :type ftp_conn_id:     string
    :param ftp_path:        The path to the file on the FTP client.
    :type ftp_path:        string
    :param s3_conn_id:      The s3 connnection id.
    :type s3_conn_id:       string
    :param s3_bucket:       The destination s3 bucket.
    :type s3_bucket:        string
    :param s3_key:          The destination s3 key.
    :type s3_key:           string
    """

    template_fields = ('s3_key',)

    def __init__(self,
                 ftp_conn_id,
                 ftp_directory,
                 local_path,
                 s3_conn_id,
                 s3_bucket,
                 s3_key,
                 *args,
                 **kwargs):
        super().__init__(*args, **kwargs)
        self.ftp_conn_id = ftp_conn_id
        self.ftp_directory = ftp_directory
        self.local_path = local_path
        self.s3_conn_id = s3_conn_id
        self.s3_bucket = s3_bucket
        self.s3_key = s3_key

    def execute(self, context):

        # In an operator, everything should be fed to the execute operator.

        # Operators use hooks for external connections.
        ftp = FTPHook(ftp_conn_id=self.ftp_conn_id)
        s3_hook = S3Hook(self.s3_conn_id)

        # Log out everything in the directory.
        logging.info(self.ftp_directory)

        self.download_file(ftp)
        self.upload_to_s3(s3_hook)

    def download_file(self, ftp):

        ftp.retrieve_file(self.ftp_directory, self.local_path)
        logging.info("Downloaded file!")

    def upload_to_s3(self, s3_hook):
        s3_hook.load_file(
            filename=self.local_path,
            key='{0}'.format(self.s3_key),
            bucket_name=self.s3_bucket,
            replace=True
        )
