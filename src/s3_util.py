import logging.config
import re
import typing

import boto3
import botocore

logger = logging.getLogger(__name__)


def parse_s3(s3path: str) -> typing.Tuple[str, str]:
    """Passe the s3 bucket name and the s3 path from a full s3 path"""
    regex = r's3://([\w._-]+)/([\w./_-]+)'

    mat = re.match(regex, s3path)
    s3bucket = mat.group(1)
    s3path = mat.group(2)

    return s3bucket, s3path


def upload_file_to_s3(local_path: str, s3path: str) -> None:
    """Upload a file from local to s3"""
    s3bucket, s3_just_path = parse_s3(s3path)

    s3 = boto3.resource('s3')
    bucket = s3.Bucket(s3bucket)

    try:
        bucket.upload_file(local_path, s3_just_path)
    except botocore.exceptions.NoCredentialsError:
        logger.error('Please provide AWS credentials via AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY env variables.')
    else:
        logger.info('Data uploaded from %s to %s', local_path, s3path)


def download_file_from_s3(local_path: str, s3path: str) -> None:
    """Download a file from s3 to local"""
    s3bucket, s3_just_path = parse_s3(s3path)

    s3 = boto3.resource('s3')
    bucket = s3.Bucket(s3bucket)

    try:
        bucket.download_file(s3_just_path, local_path)
    except botocore.exceptions.NoCredentialsError:
        logger.error('Please provide AWS credentials via AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY env variables.')
    else:
        logger.info('Data downloaded from %s to %s', s3path, local_path)
