import datetime

import sys, os
import requests
import dateutil.parser as dp
import json
from bs4 import BeautifulSoup
import pytz
import urllib

class Fmiweather:

    url = "http://opendata.fmi.fi/wfs"
    stationsFile = 'resources/fmi_met_stations.json'
    stations = []

    def __init__(self):
        self.setStations()

    
    def setStations(self):
        data = []
        with open(self.stationsFile) as json_file:  
            data = json.load(json_file)
        for station in data:
            self.stations.append(station)


    def getGetParameters(self, station, days, daysAgo):
        fromDay = datetime.date.today() - datetime.timedelta(days=daysAgo + days)
        toDay = datetime.date.today() - datetime.timedelta(days=daysAgo)
        params = {"service" : "WFS",
            "version" : "2.0.0",
            "request" : "getFeature",
            "parameters" : "TA_PT1H_AVG",
            "starttime" : fromDay.strftime('%Y-%m-%dT00:00:00Z'),
            "endtime" : toDay.strftime('%Y-%m-%dT23:59:59Z'),
            "storedquery_id" : "fmi::observations::weather::hourly::timevaluepair",
            "networkid" : "121",
            #"timezone" : "Europe/Oslo", 
            "fmisid" : str(station['id']),
        }
        return urllib.parse.urlencode(params)

    def convertTime(self, convertFrom):
        tz1 = pytz.timezone('Europe/Berlin')
        tz2 = pytz.timezone('UTC')
        temp = datetime.datetime.strptime(convertFrom, '%Y-%m-%dT%H:%M:%SZ')
        temp = tz2.localize(temp)
        temp = temp.astimezone(tz1)
        return datetime.datetime.strftime(temp, '%d/%m/%Y %H:%M:%S')

    def cleanDataFromFmi(self, jsondata, station):
        cleaned = []
        for meassurement in jsondata:
            cleaned.append([
                station['id'],
                station['name'],
                str(meassurement['time']),
                str(meassurement['temperature']),
            ])
        return cleaned

    def fetchData(self, station, days, daysAgo):
        resource = requests.get(self.url + "?" + self.getGetParameters(station, days, daysAgo))
        soup = BeautifulSoup(resource.text, 'xml')
        ms = soup.find_all('MeasurementTVP')
        jsondata = []
        for item in ms:
            jsondata.append({'time' : self.convertTime(item.time.text), 'temperature' : item.value.text})
        return self.cleanDataFromFmi(jsondata, station)

    def fetchDataFromAllStations(self, days=1, daysAgo=0):
        dataFromAllStations = []
        for station in self.stations:
            dataFromAllStations.append(self.fetchData(station, days, daysAgo))
        return dataFromAllStations

test = Fmiweather()
print(test.fetchDataFromAllStations(1, 0))
