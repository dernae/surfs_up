#start of section 5 
import datetime as dt
import numpy as np
import pandas as pd

#dependencies for sqAlchemy 
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#dependencies for flask 
from flask import Flask, jsonify

#set up our database engine for the Flask application
#The create_engine() function allows us to access and query our SQLite database file. 
engine = create_engine("sqlite:///hawaii.sqlite")

#reflect the database into our classes.
Base = automap_base()
Base.prepare(engine, reflect=True)

 #save our references to each table.
Measurement = Base.classes.measurement
Station = Base.classes.station

 #create a session link from Python to our database 
 session = Session(engine)

 #reate a Flask application called "app."
 # ame variable value depends on where and how the code is run
 app = Flask(__name__)

# If you google "surfer," for example, you'll see search options for images, videos, news, 
# maps, and more. These are all the different "routes" you can take, and the Google homepage is essentially the root.
#define the welcome route
@app.route("/")

# create a function welcome() with a return statement
#add the precipitation, stations, tobs, and temp routes that we'll need for this module into our return statement.
#se f-strings to display them 
def welcome():
    return(
    '''
    Welcome to the Climate Analysis API!
    Available Routes:
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end
    ''')

#Every time you create a new route, your code should be aligned to the left in order to avoid errors.
@app.route("/api/v1.0/precipitation")

#create the precipitation() function
#add the line of code that calculates the date one year ago from the most recent date in the database
#write a query to get the date and precipitation for the previous year.
def precipitation():
   prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
   precipitation = session.query(Measurement.date, Measurement.prcp).\
      filter(Measurement.date >= prev_year).all()
   return
# .\ : This is used to signify that we want our query to continue on the next line. You can use the combination of .\ to 
# shorten the length of your query line so that it extends to the next line.

#create a dictionary with the date as the key and the precipitation as the value. 
#Jsonify() is a function that converts the dictionary to a JSON file.
def precipitation():
   prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
   precipitation = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= prev_year).all()
   precip = {date: prcp for date, prcp in precipitation}
   return jsonify(precip)

#third route 
@app.route("/api/v1.0/stations")

#create a new function called stations()
#get all of the stations in our database. 
#unraveling our results into a one-dimensional array. To do this, we want to use thefunction np.ravel(), with results as our parameter.
#convert our unraveled results into a list. 
def stations():
results = session.query(Station.station).all()
stations = list(np.ravel(results))
return jsonify(stations=stations)
#You may notice here that to return our list as JSON, we need to add stations=stations

#create the temperature observations route.
@app.route("/api/v1.0/tobs")

#calculate the date one year ago from the last date in the database.
#query the primary station for all the temperature observations from the previous year
#unravel the results into a one-dimensional array and convert that array into a list.
#jsonify our temps list, and then return it
def temp_monthly():
prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    results = session.query(Measurement.tobs).\
filter(Measurement.station == 'USC00519281').\
filter(Measurement.date >= prev_year).all()
temps = list(np.ravel(results))
    return jsonify(temps=temps)

#create a route for our summary statistics report.
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")

#query to select the minimum, average, and maximum temperatures from our SQLite database
#query our database using the SEL list that we just made
#asterisk is used to indicate there will be multiple results for our query: minimum, average, and maximum temperatures.
#calculate the temperature minimum, average, and maximum with the start and end dates. 
def stats(start=None, end=None):
        sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]           

     if not end: 
       results = session.query(*sel).\
        filter(Measurement.date <= start).all()
           temps = list(np.ravel(results))
           return jsonify(temps)

     results = session.query(*sel).\
           filter(Measurement.date >= start).\
         filter(Measurement.date <= end).all()
     temps = list(np.ravel(results))
     return jsonify(temps=temps)