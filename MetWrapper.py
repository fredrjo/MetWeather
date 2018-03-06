from flask import Flask
from flask_restful import Resource, Api
import requests # See http://docs.python-requests.org/
import dateutil.parser as dp

class MetWrapper:

    def getObservations(stations, myElements, timeInterval):
        client_id = 'df3e5f22-545a-46d4-aeb3-bfb6b291d3f0'
        url = 'https://frost.met.no/observations/v0.jsonld'
        r = requests.get( url,
            {'sources': stations , 'elements': myElements, 'referencetime': timeInterval},
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
            iso8601 = item['referenceTime']
            myStations[iso8601] = {'station' : item['sourceId'], 'observe' : MetWrapper.printObservations(item['observations'])}
        return myStations
