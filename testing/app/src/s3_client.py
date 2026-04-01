import boto3
import logging
from botocore.exceptions import ClientError
from typing import Optional

logger = logging.getLogger(__name__)

class S3Service:
    def __init__(self, region_name: str = "us-east-1"):
        """Initialize the S3 Client"""
        try:
            self.s3_client = boto3.client('s3', region_name=region_name)
        except Exception as e:
            logger.error(f"Failed to initialize S3 client: {e}")
            raise

    def upload_file(self, file_name: str, bucket: str, object_name: Optional[str] = None) -> bool:
        """Upload a file to an S3 bucket

        :param file_name: File to upload
        :param bucket: Bucket to upload to
        :param object_name: S3 object name. If not specified then file_name is used
        :return: True if file was uploaded, else False
        """
        if object_name is None:
            object_name = file_name

        try:
            self.s3_client.upload_file(file_name, bucket, object_name)
            logger.info(f"Successfully uploaded {file_name} to {bucket}/{object_name}")
            return True
        except ClientError as e:
            logger.error(f"Error uploading file to S3: {e}")
            return False

    def download_file(self, bucket: str, object_name: str, file_name: str) -> bool:
        """Download a file from an S3 bucket

        :param bucket: Bucket to download from
        :param object_name: S3 object name
        :param file_name: File name to save to locally
        :return: True if file was downloaded, else False
        """
        try:
            self.s3_client.download_file(bucket, object_name, file_name)
            logger.info(f"Successfully downloaded {bucket}/{object_name} to {file_name}")
            return True
        except ClientError as e:
            logger.error(f"Error downloading file from S3: {e}")
            return False

s3_service = S3Service()
