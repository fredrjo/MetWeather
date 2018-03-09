from flask import Flask
from flask_restful import Resource, Api
from MetWrapper import MetWrapper
from models.StationModel import StationModel
from models.MeasurementModel import MeasurementModel
import sys

class ImportWeather(Resource):
    def get(self):
        myElements = ['air_temperature, mean(wind_speed P1D)']
        #mySources = ','.join(name for name in StationModel.getAllStationsAsString(StationModel))
        mySources = 'SN18700, SN1050'
        getDataFrom = '2018-03-04'
        getDataTo = '2018-03-09'
        dateString = getDataFrom + '/' + getDataTo
        print(mySources)
        r = MetWrapper.getObservations(mySources, myElements,dateString )

        if r.status_code == 200:
            MeasurementModel.saveMany(r.json())
            return 0#MetWrapper.printStations(r)
        else:
            sys.stdout.write('error:\n')
            sys.stdout.write('\tstatus code: {}\n'.format(r.status_code))
