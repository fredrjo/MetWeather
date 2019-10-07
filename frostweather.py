import datetime

import sys, os
import requests
import dateutil.parser as dp
import json
import pytz

class Frostweather:

    url = 'https://frost.met.no/'
    client_id = 'df3e5f22-545a-46d4-aeb3-bfb6b291d3f0'
    stationsFile = 'resources/frost_stations.json'
    dateFormat = '%Y-%m-%d %H:%M:00.000Z'
    stationsPrRequest = 20
    timeresolutions = 'PT1H'

    stations = []

    def __init__(self):
         self.setStations()

    def setStations(self):
        data = []
        with open(self.stationsFile) as json_file:  
            data = json.load(json_file)
        for station in data['stations']['data']:
            self.stations.append(station)

    def getNameForId(self, id):
        return list(filter(lambda x : x['id'] == id, self.stations ))[0]['name']

    def getNamesFromArray(self, arr):
        stations = arr[0]['id']
        for item in arr[1:]:
            stations += ',' + item['id']
        return stations

    def getStationsChunks(self, chunkSize):
        stationStrings = []
        chunks = [self.stations[i:i + chunkSize] for i in range(0, len(self.stations), chunkSize)]
        for chunk in chunks:
            stationStrings.append(self.getNamesFromArray(chunk))
        return stationStrings

    def getGetParameters(self, stations, days, daysAgo, weatherType):
        fromDay = datetime.date.today() - datetime.timedelta(days=daysAgo + days)
        toDay = datetime.date.today() - datetime.timedelta(days=daysAgo)
        referenceTime = fromDay.strftime('%Y-%m-%d') + '/' + toDay.strftime('%Y-%m-%d')
        return {
            'sources' : stations,
            'elements' : weatherType,
            'timeresolutions' : self.timeresolutions,
            'referencetime' : referenceTime
        }

    def fetchData(self, stations, days, daysAgo, weatherType):
        print(stations)
        page = requests.get(
            self.url + 'observations/v0.jsonld', 
            self.getGetParameters(stations, days, daysAgo, weatherType),
            auth=(self.client_id, '')
        )
        return self.cleanData(json.loads(page.text))

    def rearrangeDate(self, theDate, inFormat):
        tz1 = pytz.timezone('Europe/Berlin')
        tz2 = pytz.timezone('UTC')
        temp = datetime.datetime.strptime(theDate, inFormat)
        temp = tz2.localize(temp)
        temp = temp.astimezone(tz1)
        return temp.strftime(self.dateFormat)

    def cleanData(self, jsondata, station = 'Default'):
        cleaned = []
        if 'data' not in jsondata:
            return []
        for meassurement in jsondata['data']:
            cleaned.append([
                str(meassurement['sourceId'][2:-2]),
                self.getNameForId(str(meassurement['sourceId'][:-2])),
                self.rearrangeDate(str(meassurement['referenceTime']), '%Y-%m-%dT%H:%M:%S.000Z'),
                str(meassurement['observations'][0]['value']),
            ])
        return cleaned

    def fetchDataFromAllStations(self, days=1, daysAgo=0, weatherType = 'air_temperature'):
        dataFromAllStations = []
        for stations in self.getStationsChunks(self.stationsPrRequest):
            dataFromAllStations.append(self.fetchData(stations, days, daysAgo, weatherType))
        return dataFromAllStations

    def getAllStationsFromfrost(self, country_code):
        url = self.url + 'sources/v0.jsonld?types=SensorSystem&country={0}'.format(country_code)
        r = requests.get( url, {'fields' : 'id, name, geometry'},
            auth=(self.client_id, '')
        )
        return {'stations' : r.json()}
    
    def makeJsonFileForStations(self, country_code):
        stations = self.getAllStationsFromfrost(country_code)
        my_file = open(self.stationsFile, "w")
        my_file.write(json.dumps(stations, indent=4, sort_keys=True))
        my_file.close()
