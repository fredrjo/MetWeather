from flask import Flask
from flask_restful import Resource, Api
from MetWrapper import MetWrapper
from models.station import Station
from models.measurement import Measurement
from flask import request
import sys
import datetime

def list2Strings(listToSplit, chunksize):
    chunks = []
    for newChunk in range(0, len(listToSplit), chunksize):
        ele = ','.join(id for id in listToSplit[newChunk:newChunk+20]) #To many stations
        chunks.append(ele)
    return chunks

class ImportWeather(Resource):
    def get(self):
        myElements = ['air_temperature']
        mySources = list2Strings(Station.getAllStationsAsString(Station), 20)
        #mySources = ['SN50500']
        fewdaysago = datetime.date.today()- datetime.timedelta(1)
        fromDate = datetime.date.today()
        if 'days' in request.args:
            fewdaysago = datetime.date.today()- datetime.timedelta(int(request.args['days']))
        if 'daysAgo' in request.args:
            fromDate = datetime.date.today()- datetime.timedelta(int(request.args['daysAgo']))
            if 'days' in request.args:
                fewdaysago = datetime.date.today()- datetime.timedelta(int(request.args['days'])+int(request.args['daysAgo']))
        getDataFrom = fewdaysago.strftime("%Y-%m-%d")
        getDataTo = fromDate.strftime("%Y-%m-%d")
        dateString = getDataFrom + '/' + getDataTo
        allOfIt = []
        for stations in mySources:
            r = MetWrapper.getObservations(stations, myElements, dateString )
            if r.status_code == 200:
                allOfIt.append(r.json())
        Measurement.saveMany(allOfIt)
        return allOfIt
        #else:
        #    sys.stdout.write('error:\n')
        #    sys.stdout.write('\tstatus code: {}\n'.format(r.status_code))
class WeatherReport(Resource):
    def get(self):
        toDate = datetime.date.today()
        fromDate = datetime.date.today()- datetime.timedelta(int(request.args['days']))
        if 'daysAgo' in request.args:
            fromDate= datetime.date.today()- datetime.timedelta(int(request.args['daysAgo']) + int(request.args['days']))
            toDate = datetime.date.today()- datetime.timedelta(int(request.args['daysAgo']))
        if 'spesific_station' not in request.args:
            return Measurement.getAllDataFromWhere(fromDate, toDate, 'air_temperature')
        else:
            print(request.args['spesific_station'])
            return Measurement.getDataFrom(request.args['spesific_station'])
