from flask import Flask
from flask_restful import Resource, Api
from MetWrapper import MetWrapper

class ImportWeather(Resource):
    def get(self):
        myElements = ['air_temperature, mean(wind_speed P1D)']
        mySources = ['SN4780, SN50500']
        getDataFrom = '2018-03-04'
        getDataTo = '2018-03-05'
        dateString = getDataFrom + '/' + getDataTo
        r = MetWrapper.getObservations(mySources, myElements,dateString )

        if r.status_code == 200:
            return MetWrapper.printStations(r)
        else:
            sys.stdout.write('error:\n')
            sys.stdout.write('\tstatus code: {}\n'.format(r.status_code))
