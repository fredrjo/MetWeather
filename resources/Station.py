from flask import Flask
from flask_restful import Resource, Api
from models.StationModel import StationModel
class Station(Resource):
    def get(self):
        return StationModel.getStationsFromMet()
