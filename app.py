import logging.config

import joblib
from flask import Flask, render_template, request, redirect, url_for

from src.app_util import count_down
# For setting up the Flask-SQLAlchemy database session
# from src.ex_add_songs import Tracks, TrackManager
from src.sql_util import RecordManager, ModelOutputs

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

print(app.config["SQLALCHEMY_DATABASE_URI"])


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/prediction/<record_id>')
def show_prediction(record_id):
    outputs = record_manager.session.query(ModelOutputs).filter(ModelOutputs.record_id == record_id)
    return render_template('prediction.html', outputs=outputs)


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
    model_input = [airline, source, 'Evening', stops, destination, flight_class, duration, days_left]
    record_id = record_manager.unique_id()
    record_manager.add_user(id=record_id,
                            airline=airline,
                            source=source,
                            depart_time=depart_time,
                            stops=stops,
                            destination=destination,
                            flight_class=flight_class,
                            duration=duration,
                            days_left=days_left,
                            cur_price=cur_price)
    logger.info('New user record added.')
    model_input = count_down(model_input)
    model_input = encoder.transform(model_input).astype('float')
    output = model.predict(model_input)
    record_manager.add_all_output(record_id, int(days_left), output)

    return redirect(url_for('show_prediction', record_id=record_id))


if __name__ == '__main__':
    app.run(debug=app.config["DEBUG"], port=app.config["PORT"],
            host=app.config["HOST"])
    # print
