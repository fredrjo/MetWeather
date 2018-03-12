from flask import Flask
from flask_restful import Resource, Api
from models.StationModel import StationModel
from models.MeasurementModel import MeasurementModel
from flask import request
import json
class Station(Resource):
    # get all stations from Met and set flag if they have hoourly theseHaveHourTemp

    def get(self):
        letMeCheck=[]
        hasHourTemp = StationModel.getOperational()
        allStations = StationModel.getStationsFromMet()
        for st in allStations['data']:
            if st['id'] in hasHourTemp:
                st['hasHourTemp'] = True
            else:
                st['hasHourTemp'] = False
            letMeCheck.append(st)
        StationModel.saveManyStaions(letMeCheck)
        return letMeCheck

class StationS(Resource):
    def get(self):
        return StationModel.getAllStations(StationModel)

class StationOverview(Resource):
    def get(self):
        hey = MeasurementModel.getDataFrom(request.args['id'])
        return hey
        #return json.dumps(hey)

class StationOptions(Resource):
    def get(self):
        return StationModel.getStationOptions(request.args['id'])
