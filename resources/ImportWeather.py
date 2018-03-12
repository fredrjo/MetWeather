from flask import Flask
from flask_restful import Resource, Api
from MetWrapper import MetWrapper
from models.StationModel import StationModel
from models.MeasurementModel import MeasurementModel
from flask import request
import sys
import datetime

class ImportWeather(Resource):
    def get(self):
        myElements = ['air_temperature']
        
        #mySources = 'SN18700, SN1050'
        #mySources = request.args['id']
        fewdaysago = datetime.date.today()- datetime.timedelta(1)
        getDataFrom = fewdaysago.strftime("%Y-%m-%d")
        getDataTo = datetime.date.today().strftime("%Y-%m-%d")
        dateString = getDataFrom + '/' + getDataTo
        mySources = ','.join(id for id in StationModel.getAllStationsAsString(StationModel)) #To many stations
        print(mySources)
        #print(mySources)
        chunksize = 20
        allOfIt = []
        for newChunk in range(0, len(mySources), chunksize):
            chunk = mySources[newChunk:newChunk+chunksize]
            r = MetWrapper.getObservations(chunk, myElements,dateString )
            if r.status_code == 200:
                allOfIt.append(r.json())
        MeasurementModel.saveMany(allOfIt)

        return allOfIt
        #else:
        #    sys.stdout.write('error:\n')
        #    sys.stdout.write('\tstatus code: {}\n'.format(r.status_code))
