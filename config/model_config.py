# Data path
RAW_DATA_PATH = "data/raw/flight_data.csv"
S3_DATA_PATH = "s3://2022-msia423-zhao-ruyang/raw/flight_data.csv"
LOCAL_DATA_PATH = "data/sample/flight_data.csv"
CLEANED_DATA_PATH = "data/clean/clean_data.csv"

# Preprocess config
COLUMN_TO_MODIFY = "stops"
COLUMN_TO_DROP = ["flight", "arrival_time"]

# Model config
MODEL_PATH = "models/model.joblib"
