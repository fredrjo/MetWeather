import sys, os
from flask import Flask
from flask_restful import Resource, Api
from flask_cors import CORS

from models.station import Station
from models.measurement import Measurement
from resources.ImportWeather import ImportWeather, WeatherReport
from resources.CheckForUpdates import CheckForUpdates
from resources.api_station import ImportStations, AllStation, StationOverview, StationOptions
from MetWrapper import MetWrapper

app = Flask(__name__)

CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://grabber:@localhost/metweather'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()


api.add_resource(ImportWeather, '/weather') # Collects weather from Met get days and daysAgo
api.add_resource(WeatherReport, '/report') #need days (last days) might get daysAgo
api.add_resource(ImportStations, '/importstations')
api.add_resource(AllStation, '/stations') # Get all relevant stations
api.add_resource(StationOverview, '/info') # need id
api.add_resource(StationOptions, '/options') #need id

api.add_resource(CheckForUpdates, '/check')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(debug=True, host='0.0.0.0', port=5300)
