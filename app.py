import logging.config

import joblib
from flask import Flask, render_template, request, redirect, url_for
# import matplotlib.pyplot as plt
from src.app_util import count_down, time_of_day, plot_json
# For setting up the Flask-SQLAlchemy database session
# from src.ex_add_songs import Tracks, TrackManager
from src.sql_util import RecordManager, ModelOutputs
import sqlalchemy


# Initialize the Flask application
app = Flask(__name__, template_folder="app/templates",
            static_folder="app/static")

# Configure flask app from flask_config.py
app.config.from_pyfile('config/flaskconfig.py')

# Define LOGGING_CONFIG in flask_config.py - path to config file for setting
# up the logger (e.g. config/logging/local.conf)
logging.config.fileConfig(app.config["LOGGING_CONFIG"])
logger = logging.getLogger(app.config["APP_NAME"])
logger.debug(
    'Web app should be viewable at %s:%s if docker run command maps local '
    'port to the same port as configured for the Docker container '
    'in config/flaskconfig.py (e.g. `-p 5000:5000`). Otherwise, go to the '
    'port defined on the left side of the port mapping '
    '(`i.e. -p THISPORT:5000`). If you are running from a Windows machine, '
    'go to 127.0.0.1 instead of 0.0.0.0.', app.config["HOST"]
    , app.config["PORT"])

# Initialize the database session
record_manager = RecordManager(app)

# record_manager = RecordManager(app.config["SQLALCHEMY_DATABASE_URI"])
encoder = joblib.load('models/encoder.joblib')
model = joblib.load('models/model.joblib')


@app.route('/')
def index():
    # pr(
    return render_template('index.html')


@app.route('/prediction/<record_id>')
def show_prediction(record_id):
    outputs = record_manager.session.query(ModelOutputs).filter(ModelOutputs.record_id == record_id)
    days = [output.days_left for output in outputs]
    price = [output.price for output in outputs]
    graph_pred = plot_json(days, price)

    return render_template('prediction.html', graphJSON=graph_pred, outputs=outputs)


@app.route('/predict', methods=['POST'])
def predict_price():
    """View that process a POST with new user input

    Returns:
        redirect to index page
    """
    airline = request.form['airline']
    source = request.form['source']
    depart_time = request.form['depart_time']
    stops = request.form['stops']
    destination = request.form['destination']
    flight_class = request.form['flight_class']
    duration = request.form['duration']
    days_left = request.form['days_left']
    cur_price = request.form['cur_price']
    model_input = [airline, source, time_of_day(depart_time), stops, destination, flight_class, duration, days_left]
    # Get a unique id for the user record
    logger.info(model_input)
    try:
        record_id = record_manager.unique_id()
    except sqlalchemy.exc.OperationalError as e:
        logger.error('Unable to get ids from the user_records table. Check network.')
        logger.error(e)
        return render_template('error.html', msg='Unable to connect to the database. Please check network.')
    # pri(
    except sqlalchemy.exc.SQLAlchemyError as e:
        logger.error('Unable to get ids from the user_records table')
        logger.error(e)
        return render_template('error.html', msg='Unable to connect to the database.')
    else:
        logger.debug('Successfully get all id\'s from the user_records table.')
    # Add the user record to database
    try:
        record_manager.add_user(_id=record_id,
                                airline=airline,
                                source=source,
                                depart_time=depart_time,
                                stops=stops,
                                destination=destination,
                                flight_class=flight_class,
                                duration=duration,
                                days_left=days_left,
                                cur_price=cur_price)
    except sqlalchemy.exc.OperationalError as e:
        logger.error('Unable to add record with id %s to the user_records table. Check network.', record_id)
        logger.error(e)
        return render_template('error.html', msg='Unable to access to the database. Please check network.')
    except sqlalchemy.exc.SQLAlchemyError as e:
        logger.error('Unable to add record with id %s to the user_records table.', record_id)
        logger.error(e)
        return render_template('error.html', msg='Unable to access to the database.')
    else:
        logger.info('Successfully added record with id %s to the user_records table.', record_id)

    # Get input data with days left count down to 0
    model_input = count_down(model_input)
    # Onehot encode the input data
    try:
        model_input = encoder.transform(model_input).astype('float')
    except AttributeError as e:
        logger.error('Unable to onehot encode the model_input.')
        logger.error(e)
        return render_template('error.html', msg='Unable to process the input. Check input.')
    else:
        logger.info('Successfully onehot encoded the model input for id %s', record_id)
        # Redirect to the error page
    # Predict prices
    try:
        output = model.predict(model_input)
    except ValueError as e:
        logger.error('Model_input does not have correct number of dimensions.')
        logger.error(e)
        return render_template('error.html', msg='Unable to process the input. Check input.')
    else:
        logger.info('Successfully predicted prices for for id %s', record_id)
        logger.debug('There are %s predictions made.', len(model_input))
    # Add model outputs to database
    try:
        record_manager.add_all_output(record_id, int(days_left), output)
    except sqlalchemy.exc.OperationalError as e:
        logger.error('Unable to add model output with id %s to the model_outputs table. '
                     'Check network.', record_id)
        logger.error(e)
        return render_template('error.html', msg='Unable to access to the database. Please check network.')
    except sqlalchemy.exc.SQLAlchemyError as e:
        logger.error('Unable to add model output with id %s to the model_outputs table.',
                     record_id)
        logger.error(e)
        return render_template('error.html', msg='Unable to access to the database.')
    else:
        logger.info('Successfully added price predictions for id %s to the model_outputs table.',
                    record_id)

    return redirect(url_for('show_prediction', record_id=record_id))


if __name__ == '__main__':
    app.run(debug=app.config["DEBUG"], port=app.config["PORT"],
            host=app.config["HOST"])
