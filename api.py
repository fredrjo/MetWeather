import sys, os
from flask import Flask
from flask_restful import Resource, Api

from models.StationModel import StationModel
from models.MeasurementModel import MeasurementModel
from resources.ImportWeather import ImportWeather
from resources.CheckForUpdates import CheckForUpdates
from resources.Station import Station
from MetWrapper import MetWrapper

app = Flask(__name__)
api = Api(app)

api.add_resource(ImportWeather, '/')
api.add_resource(Station, '/station')

api.add_resource(CheckForUpdates, '/check')

if __name__ == '__main__':
    app.run(debug=True)
