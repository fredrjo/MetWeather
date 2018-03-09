from flask import Flask
from flask_restful import Resource, Api
from models.StationModel import StationModel
from models.MeasurementModel import MeasurementModel
class Station(Resource):
    def get(self):
        return StationModel.getStationsFromMet()


class StationS(Resource):
    def get(self):
        return StationModel.getAllStations(StationModel)

class StationOverview(Resource):
    def get(self):
        hey = MeasurementModel.getDataFrom('SN18700')
        print(hey.value)
        return hey.value
