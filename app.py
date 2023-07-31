# Import the dependencies.
import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################

# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement=Base.classes.measurement
Station=Base.classes.station

# Create our session (link) from Python to the DB
session=Session(engine)

#################################################
# Flask Setup
#################################################

app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    return (
        f"Welcome to the Anastasia API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    previous=dt.date(2017,8,23)-dt.timedelta(days=365)
    results=session.query(Measurement.date,Measurement.prcp).filter(Measurement.date >=previous).all()
    precip = {date:prcp for date, prcp in results}
    return jsonify(precip)


@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)


@app.route("/api.v1.0/tobs")
def tobs():
    previous=dt.date(2017,8,23)-dt.timedelta(days=365)
    tobs_data = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= previous()).all()
    tobs_list = []
    for date, tobs in tobs_data:
        tobs_dctnr = {}
        tobs_dctnr["date"] = date
        tobs_dctnr["tobs"] = tobs
        tobs_list.append(tobs_dctnr)
    return jsonify(tobs_list)
    

@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def cal_temp(start=None, end=None):
    mamtemps=[func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    if end == None: 
        start_data = session.query(*sel).\
        filter(Measurement.date >= start).all()
        start_list = list(np.ravel(start_data))
        return jsonify(start_list)
    else:
        start_end_data = session.query(*sel).\
            filter(Measurement.date >= start).\
            filter(Measurement.date <= end).all()
        start_end_list = list(np.ravel(start_end_data))
        return jsonify(start_end_list)



if __name__ == "__main__":
    app.run(debug=True)
