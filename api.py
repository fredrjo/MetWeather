import sys, os
from flask import Flask
from flask_restful import Resource, Api
from flask_cors import CORS

from models.StationModel import StationModel
from models.MeasurementModel import MeasurementModel
from resources.ImportWeather import ImportWeather
from resources.CheckForUpdates import CheckForUpdates
from resources.Station import Station, StationS
from MetWrapper import MetWrapper

app = Flask(__name__)
api = Api(app)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


api.add_resource(ImportWeather, '/')
api.add_resource(Station, '/station')
api.add_resource(StationS, '/stations')

api.add_resource(CheckForUpdates, '/check')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(debug=True)
