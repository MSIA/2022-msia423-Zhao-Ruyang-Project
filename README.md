# MSiA423 Template Repository

# Table of Contents
* [Project charter ](#Project-charter)
* [Running the app ](#Running-the-app)
	* [1. Initialize the database ](#1.-Initialize-the-database)
	* [2. Configure Flask app ](#2.-Configure-Flask-app)
	* [3. Run the Flask app ](#3.-Run-the-Flask-app)
* [Testing](#Testing)
* [Mypy](#Mypy)
* [Pylint](#Pylint)



## Project charter

### Vision

The price of flight tickets differs a lot based on the 
departure/destination cities, seat classes and airlines, etc. 
Moreover, the price of the same flight fluctuates a lot as it 
approaches the departure date.   
As a result, figuring out what is the best time to purchase a 
flight ticket can be a confusing task for customers who want 
to minimize their cost. The initial idea of developing this app 
comes from the intention to help the customers with a tight 
budget to reduce the cost of flight tickets by purchasing smartly.

### Mission

The users would be able to input flight information including departure/destination cities, seat classes, airlines, departure time and days left before departure. The app could predict the price of the flight tickets based on the information given.  
Alternatively, the app could also plot the predicted flight fare over the number of days left before departure. The ultimate goal is to enable the users to plan ahead and pick the day with the lowest fare to purchase flight tickets.  
The training data is from kaggle, and contains flight information, timestamp, and the fare at the time of parsing. The data can be accessed at https://www.kaggle.com/datasets/promptcloud/easemytrip-flight-fare-travel-listings. 

### Success criteria
There are two success criteria for assessment: the prediction performance of the machine learning model, and the engagement and retention metric of the users.  
#### Machine learning performance metric
To evaluate the performance of the model, MAPE (Mean Absolute Percentage Error) is used, and the initial goal is to have MAPE below 10%.  

#### Business metric
To understand how appealing the app is to the users, several metrics are used to measure users' engagement and retention:
1. Number of predictions per user per month
2. Average time spent on the app
3. Month one retention of the users, i.e. percentage of users who remain active one month after they sign up

The app could be considered successful if month one retention surpass 50%, and average number of predictions per month is over 1 for each user.


```
├── README.md                         <- You are here
├── app
│   ├── static/                       <- CSS, JS files that remain static
│   ├── basic.css    			  	  <- CSS file to set the style for html pages
├── templates/                    	  <- HTML (or other code) that is templated and changes based on a set of inputs│    
│	├── error.html				      <- Rrror page template
│	├── index.html				      <- Index page template
│	├── prediciton.html			      <- prediction page template
├── config                            <- Directory for configuration files 
│   ├── local/                        <- Directory for keeping environment variables and other local configurations that *do not sync** to Github 
│   ├── logging/                      <- Configuration of python loggers
│   	├── local.conf				  <- Confiuration file for python loggers
│   ├── flaskconfig.py                <- Configurations for Flask API 
│   ├── model_config.yaml		  	  <- Configuration file containing all the arguments for model pipeline
│
├── data                              <- Folder that contains data used or generated. Only the external/ and sample/ subdirectories are tracked by git. 
│   ├── raw/                     	  <- Raw data sources, used to upload to S3 to mimic the data acquisition process
│   ├── download/                     <- Directory for raw data loaded from s3 to start model pipeline
│   ├── clean/ 						  <- Directory for cleaned data after being preprocessed
│   ├── train/						  <- Directory for training data
│   ├── test/						  <- Directory for testing data
│   ├── prediction/					  <- Directory for model prediction 
│
├── deliverables/                     <- Any white papers, presentations, final work products that are presented or delivered to a stakeholder 
│   ├── Flight Price Prediction.pdf   <- Presentation slides for the flight prediction app
│
├── docs/                             <- Sphinx documentation based on Python docstrings. Optional for this project.
│
├── dockerfiles/                      <- Directory for all project-related Dockerfiles 
│   ├── Dockerfile                	  <- Dockerfile for building image to execute `run.py` `run_s3.py` and `run_rds.py` 
│   ├── Dockerfile.app                <- Dockerfile for building image to run web app
│   ├── Dockerfile.test               <- Dockerfile for building image to run unit tests
│
├── evaluations						  <- Directory for saving the model evaluation metrics
│
├── figures/                          <- Generated graphics and figures to be used in reporting, documentation, etc
│
├── models/                           <- Trained model objects (TMOs), model predictions, and/or model summaries
│
├── notebooks/
│   ├── archive/                      <- Develop notebooks no longer being used.
│   ├── deliver/                      <- Notebooks shared with others / in final state
│   ├── develop/                      <- Current notebooks being used in development.
│   ├── template.ipynb                <- Template notebook for analysis with useful imports, helper functions, and SQLAlchemy setup. 
│
├── reference/                        <- Any reference material relevant to the project
│
├── src/                              <- Source data for the project. No executable Python files should live in this folder.  
│
├── test/                             <- Files necessary for running model tests (see documentation below) 
│   ├──	test_app_util.py			  <- Tests for app_util module
│   ├── test_preprocess_util.py		  <- Tests for preprocess_util module
│
├── app.py                            <- Flask wrapper for running the web app 
├── run.py                            <- Simplifies the execution of one or more of the src scripts  
├── run_rds.py                        <- Create relevant tables in the database
├── run_s3.py                         <- Upload or download raw data to or from s3 bucket
├── requirements.txt                  <- Python package dependencies 
├── Makefile						  <- Make commands to execute and dependencies among the generated files
```

## Environment Setup

### AWS Credential

You need to have two environment variables - `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`  setup in your computer to run the following commands with S3. A simple way to do this run the following two lines in your terminal shell. Note that you need to replace "YOUR_ACCESS_KEY_ID" and "YOUR_SECRET_ACCESS_KEY" to your real id and secret access key. 

```bash
export AWS_ACCESS_KEY_ID="YOUR_ACCESS_KEY_ID"
export AWS_SECRET_ACCESS_KEY="YOUR_SECRET_ACCESS_KEY"
```

### RDS Credential
##### Database Connection URI

You need to define an environment variable call `SQLALCHEMY_DATABASE_URI` to create database and ingest data into the remote database. The format for this URI is described below.  

```bash
export SQLALCHEMY_DATABASE_URI = "YOUR_DATABASE_URI"
```
## Docker
###Images

The project needs three docker images to execute the python files
1. Dockerfile: to run all steps related to training the model 
2. Dockerfile.app: to run the web app
3. Dockerfile.test: to run tests for eligible functions used in the project

###Build Images
Run following commands to build the above images
```bash
make image-model
make image-app
make image-test
```
+ The `make image-model` will produce a Docker image called `final-project`, which are used to get the raw data, run the model pipeline, and interact with database. 
+ The `make image-app` will produce a Docker image called `final-project-app`, which are used to launch the flask app. 
+ The `make image-test` will produce a Docker image called `final-project-tests`, which are used to run the test 

## Model
### Run Entire Pipeline
After building the images, you can run the entire model pipeline using the following command
```bash
make model-pipeline
```
This command will run the whole model pipeline, including downloading the raw data from s3, preprocessing the data, training the model and generating saving the model object. The final output is stored in `evaluations/report.txt`. Next, we will describe how to run each step in the pipeline and the location of artifacts produced from each step. Note that those four steps below need to be run sequentially. 
+ A SQLAlchemy database connection is defined by a string with the following format:

`dialect+driver://username:password@host:port/database`

The `+dialect` is optional and if not provided, a default is used. For a more detailed description of what `dialect` and `driver` are and how a connection is made, you can see the documentation [here](https://docs.sqlalchemy.org/en/13/core/engines.html). 


Q: Organizations of rds and s3, where to put credentials ENV?,
using raw sql queries.

### Download Raw Data from S3

You can download the data from s3 to local with `make acquire-data`. The default `S3_PATH` is `s3://2022-msia423-zhao-ruyang/raw/flight_data.csv`. This step will store the raw data to `data/download/flight_data.csv`.

### Preprocess Data

You can preprocess the data with `make preprocess`, which will store the preprocessed data to `data/clean/clean_data.csv`.

### Generate Features

You can generate features with one-hot encoding and save the onehot encoder with `make generate-feature`, which will save the features and target in `data/clean/features.npy` and `data/clean/target.npy`, also save the encoder in `models/encoder.joblib`.

### Train Model

You can train the model with `make train`, which will store the trained model to `models/model.joblib`.

### Generate Predictions

You can generate the model predictions on test data with `make score`, which will store the results in `data/predictions/prediction.npy`.

### Evaluate the model

You can generate evaluation metrics for the model with `make evaluate`, which will store the evaluation in `evaluations/report.txt`

## Create Database
The web app needs a SQL database to run. To create the relevant tables in your database, run following command.
```bash
make create-db
```
You can also create a local SQLite database to test the app by passing a SQLite engine string to the environment varialbe `SQLALCHEMY_DATABASE_URI`. It does not require a username or password and replaces the host and port with the path to the database file, and it takes the following form: 

```python
'sqlite:///data/flight.db'
```

The three `///` denote that it is a relative path to where the code is being run (which is from the root of this directory).

You can also define the absolute path with four `////`, for example:

```python
'sqlite://///Users/cmawer/Repos/2022-msia423-template-repository/data/tracks.db'
```

If no `SQLALCHEMY_DATABASE_URI` environment variable is found, a default SQLite engine string `sqlite:///data/flight.db` is used to create a local database.

## Running the app
Before running the app, make sure you have completed the following:
1. Set environment variables properly according to the above guidelines.
2. Build docker image `final-project-app` by running `make image-app`.
3. Run the entire model pipeline either by `make model-pipeline` or executing each step sequentially with the corresponding `make` command. 
4. Create the relevant tables in the database connected via your `SQLALCHEMY_DATABASE_URI` environment variable . This can be done by running `make create-db`. 

### 1. Configure Flask app
`config/flaskconfig.py` holds the configurations for the Flask app. It includes the following configurations:

```python
import os
DEBUG = True  # Keep True for debugging, change to False when moving to production 
LOGGING_CONFIG = "config/logging/local.conf"  # Path to file that configures Python logger
HOST = "0.0.0.0" # the host that is running the app. 0.0.0.0 when running locally 
PORT = 5001  # What port to expose app on. Must be the same as the port exposed in dockerfiles/Dockerfile.app 
APP_NAME = 'flight-price-prediction'
SQLALCHEMY_TRACK_MODIFICATIONS = True #If set to True, Flask-SQLAlchemy will track modifications of objects and emit signals.
SQLALCHEMY_ECHO = False  # If true, SQL for queries made will be printed

SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
if SQLALCHEMY_DATABASE_URI is None:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///data/flight.db' # URI (engine string) for database that contains relevant tables
```

### 2. Run the Flask app

To run the Flask app, run: 

```bash
 make run-app
```
You should be able to access the app at http://127.0.0.1:5001/ in your browser (Mac/Linux should also be able to access the app at http://127.0.0.1:5001/ or localhost:5001/) .

Note: If `PORT` in `config/flaskconfig.py` is changed, this port should be changed accordingly (as should the `EXPOSE 5001` line in `dockerfiles/Dockerfile.app`)


#### Kill the container 

Once finished with the app, you will need to kill the container. If you named the container, you can execute the following: 

```bash
docker kill test-app 
```
where `test-app` is the name given in the `docker run` command.

If you did not name the container, you can look up its name by running the following:

```bash 
docker container ls
```

The name will be provided in the right most column. 

## Testing

Run the following:

Once you have built the image `final-project-tests` for testing by running `make image-test`. You can run the following to do uint tests: 

```bash
 make run-test
```

The following command will be executed within the container to run the provided unit tests under `test/`:  

```bash
python -m pytest
```

## Pylint

Build the image for running pylint:

```bash
 docker build -f dockerfiles/Dockerfile.pylint -t final-project-pylint .
```

To run pylint for a file, run:

```bash
 docker run final-project-pylint run.py 
```

(or any other file name, with its path relative to where you are executing the command from)

To allow for quick iteration, mount your entire repo so changes in Python files are detected:


```bash
 docker run --mount type=bind,source="$(pwd)"/,target=/app/ final-project-pylint run.py
```