from flask import Flask
from flask_restful import Resource, Api
import requests # See http://docs.python-requests.org/
import dateutil.parser as dp

class MetWrapper:

    baseUrl = 'https://frost.met.no/'
    client_id = 'df3e5f22-545a-46d4-aeb3-bfb6b291d3f0'


    def getObservations(stations, myElements, timeInterval):
        url = MetWrapper.baseUrl + 'observations/v0.jsonld'
        r = requests.get( url,
            {'sources': {stations} , 'elements': myElements, 'referencetime': timeInterval},
            #{'elements': myElements, 'timeresolutions' : 'PT1H', 'referencetime': timeInterval},
            auth=(MetWrapper.client_id, '')
            )
        print (r)
        print(stations)
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

    def getOptionsFromMet(station_id):
        url = MetWrapper.baseUrl + 'observations/availableTimeSeries/v0.jsonld'
        #r = requests.get( url, {'sources' :{station_id}, 'referencetime' :'2017-01-01'}, auth=(client_id, ''))
        r = requests.get( url, {'elements' : 'air_temperature', 'timeresolutions' :'PT1H', 'referencetime' :'2017-01-01'}, auth=(MetWrapper.client_id, ''))
        return r.json()

    def getStationsWithElementAndResolution(myElement = 'air_temperature', myTimeResolution = 'PT1H'):
        url = MetWrapper.baseUrl +'observations/availableTimeSeries/v0.jsonld'
        #r = requests.get( url, {'sources' :{station_id}, 'referencetime' :'2017-01-01'}, auth=(client_id, ''))
        r = requests.get( url, {'elements' : myElement, 'timeresolutions' :myTimeResolution, 'referencetime' :'2017-01-01'}, auth=(MetWrapper.client_id, ''))
        return r.json()

    def getStationsFromMet(country_code):
        url = MetWrapper.baseUrl + 'sources/v0.jsonld?types=SensorSystem&country={0}'.format(country_code)
        # issue an HTTP GET request
        r = requests.get( url, {'fields' : 'id, name, geometry'},#{'geometry' : 'POLYGON((10 60, 10 65, 11 65, 10 60))'},
        #   {'sources': mySources , 'elements': myElements, 'referencetime': timeInterval},
            auth=(MetWrapper.client_id, '')
        )

        return r.json()
