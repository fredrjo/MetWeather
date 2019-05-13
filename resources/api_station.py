from flask import Flask
from flask_restful import Resource, Api
from models.station import Station
from models.measurement import Measurement
from flask import request
import json
class ImportStations(Resource):
    # get all stations from Met and set flag if they have hoourly theseHaveHourTemp

    def get(self):
        letMeCheck=[]
        print(request.args['country_code'])
        hasHourTemp = Station.getOperational()
        allStations = Station.getStationsFromMet(request.args['country_code'])
        for st in allStations['data']:
            if st['id'] in hasHourTemp:
                st['hasHourTemp'] = True
            else:
                st['hasHourTemp'] = False
            letMeCheck.append(st)
        Station.saveManyStaions(letMeCheck)
        return letMeCheck

class AllStation(Resource):
    def get(self):
        return Station.getAllStations(Station)

class StationOverview(Resource):
    def get(self):
        hey = Measurement.getDataFrom(request.args['id'])
        return hey
        #return json.dumps(hey)

class StationOptions(Resource):
    def get(self):
        return Station.getStationOptions(request.args['id'])
