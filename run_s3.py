import argparse
import logging.config

from config.flaskconfig import LOGGING_CONFIG, LOCAL_DATA_PATH, S3_DATA_PATH
from src.s3_util import download_file_from_s3, upload_file_to_s3

logging.config.fileConfig(LOGGING_CONFIG)
logger = logging.getLogger('run_s3.py')

parser = argparse.ArgumentParser()
parser.add_argument('--download', default=False, action='store_true',
                    help="If True, will download the data from S3. If False, will upload data to S3")
parser.add_argument('--s3_path', default=S3_DATA_PATH,
                    help="s3 data path to download or upload data")
parser.add_argument('--local_path', default=LOCAL_DATA_PATH,
                    help="local data path to store or upload data")
args = parser.parse_args()

if args.download:
    download_file_from_s3(args.local_path, args.s3_path)
else:
    upload_file_to_s3(args.local_path, args.s3_path)
