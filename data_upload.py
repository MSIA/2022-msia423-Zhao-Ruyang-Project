import boto3
import botocore
import logging.config


# Create a logger and specify the configurations
logging.config.fileConfig('./config/logging/local.conf')
logger = logging.getLogger('data_upload.py')

s3 = boto3.resource('s3')
# # Get all the bucket names
# buckets = [bucket.name for bucket in s3.buckets.all()]


try:
    s3.meta.client.upload_file('data/external/flights_fares_data.csv', '2022-msia423-zhao-ruyang', 'flights_fares.csv')
except botocore.exceptions.NoCredentialsError as e:
    logger.error('Unable to find credentials in the current environment.')
    raise e
except boto3.exceptions.S3UploadFailedError as e:
    logger.error('Unable to upload the the file, the specified bucket does not exist.')
    raise e
except FileNotFoundError as e:
    logger.error('Unable to find the file in the specified path.')

