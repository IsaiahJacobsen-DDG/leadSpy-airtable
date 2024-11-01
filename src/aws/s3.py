import json
import boto3
import logging
import botocore.exceptions
from ..slack.slack_error_messages import slack_error_handler

logging.basicConfig(level=logging.INFO)


class Bucket:
    """
    Responsible for all simple storage solution interactions
    """

    def __init__(self):
        self.s3_client = boto3.client('s3')
        self.lambda_name = 'lspy-exact-phrase-priority-1'

    @slack_error_handler
    def read_bucket(self, bucket, file) -> dict:
        """
        Helper function to read s3 buckets
        :param bucket: s3 bucket name
        :param file: File name to read from bucket
        :return: Dictionary contents of the target file
        """
        try:
            response = self.s3_client.get_object(Bucket=bucket, Key=file)
            content = response['Body'].read().decode('utf-8')
            return json.loads(content)
        except botocore.exceptions.ClientError as error:
            logging.error(f'AWS Client Error: Unable to read {file} in {bucket}. Error: {error}')
            raise

    @slack_error_handler
    def write_bucket(self, data, bucket_name, file_name, content_type='application/json'):
        """
        Helper function that writes content to a s3 file
        :param data: data to write to s3
        :param bucket_name: s3 bucket to send file to
        :param file_name: Name of data file
        :param content_type: Format to write file in
        :return: Status code
        """
        try:
            self.s3_client.put_object(
                Bucket=bucket_name,
                Key=file_name,
                Body=json.dumps(data, indent=2),
                ContentType=content_type
            )

        except botocore.exceptions.ClientError as error:
            logging.error(f'Unable to push data to {bucket_name}. Error: {error}')
            return None
        else:
            return {
                'statusCode': 200,
                'body': json.dumps({'message': 'Data uploaded successfully', 's3_key': bucket_name})
            }
