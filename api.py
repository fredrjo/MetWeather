from flask import Flask
from flask_restful import Resource, Api

import sys, os
import requests # See http://docs.python-requests.org/

import dateutil.parser as dp

from models.StationModel import StationModel
from models.MeasurementModel import MeasurementModel

app = Flask(__name__)
api = Api(app)

#Constants
client_id = 'df3e5f22-545a-46d4-aeb3-bfb6b291d3f0'
url = 'https://frost.met.no/observations/v0.jsonld'

myElements = ['air_temperature, mean(wind_speed P1D)']
mySources = ['SN18700, SN4780, SN50500']
getDataFrom = '2018-03-04'
getDataTo = '2018-03-05'

def getObservations(stations, elements, timeInterval):
# issue an HTTP GET request
    r = requests.get( url,
        {'sources': mySources , 'elements': myElements, 'referencetime': timeInterval},
        auth=(client_id, '')
        )
    return r

def printObservations(observations):
    currentObservations = {}
    for item in observations:
        currentObservations[item['elementId']] = item['value']
    return currentObservations

def printStations(req):
    myStations = {}
    for item in req.json()['data']:
        #return req.json()['data']
        iso8601 = item['referenceTime']
        myStations[iso8601] = {'station' : item['sourceId'], 'observe' : printObservations(item['observations'])}
    return myStations

class ImportWeather(Resource):
    def get(self):
        dateString = getDataFrom + '/' + getDataTo
        r = getObservations(mySources, myElements, dateString )

        if r.status_code == 200:
            return printStations(r)
        else:
            sys.stdout.write('error:\n')
            sys.stdout.write('\tstatus code: {}\n'.format(r.status_code))

api.add_resource(ImportWeather, '/')

if __name__ == '__main__':
    app.run(debug=True)
