import datetime

import sys, os
import requests
import dateutil.parser as dp
import json
from bs4 import BeautifulSoup
import pytz

class Dkmetweather:

    url = 'https://wow.metoffice.gov.uk/observations/details/tableviewdata/'
    stationsFile = 'resources/dk_met_stations.json'
    dateFormat = '%Y-%m-%d %H:%M:00.000Z'

    stations = []

    def __init__(self):
         self.setStations()

    def setStations(self):
        data = []
        with open(self.stationsFile) as json_file:  
            data = json.load(json_file)
        for station in data['stations']:
            self.stations.append(station)

    def getGetParameters(self, days, daysAgo, weatherType, startAt):
        fromDay = datetime.date.today() - datetime.timedelta(days=daysAgo + days)
        toDay = datetime.date.today() - datetime.timedelta(days=daysAgo)
        return '/details/{}?startAt={}&hours=23:59:59&firstDate={}&lastDate={}&fields={}&timezone=Europe/Oslo'.format(
            fromDay.strftime('%Y-%m-%d'),
            str(startAt),
            fromDay.strftime('%Y-%m-%d'),
            toDay.strftime('%Y-%m-%d'),
            weatherType
        )

    def fetchData(self, station, days, daysAgo, weatherType, startAt):
        link = self.url + station['id'] + self.getGetParameters(days, daysAgo, weatherType, startAt)
        lol = []
        page = requests.get(link)
        closer = json.loads(page.text)
        for item in closer['Observations']:
          if ('dryBulbTemperature_Celsius' in item):
            lol.append({'time' : item['ReportStartDateTime'], 'temperature' : item['dryBulbTemperature_Celsius']})
        return self.cleanDataFromWow(lol, station)

    def rearrangeDate(self, theDate, inFormat):
        tz1 = pytz.timezone('Europe/Berlin')
        tz2 = pytz.timezone('UTC')
        temp = datetime.datetime.strptime(theDate, inFormat)
        temp = tz1.localize(temp)
        temp = temp.astimezone(tz2)
        return temp.strftime(self.dateFormat)

    def cleanDataFromWow(self, jsondata, station):
        cleaned = []
        for meassurement in jsondata:
            cleaned.append([
                station['id'],
                station['name'],
                self.rearrangeDate(str(meassurement['time']), '%Y-%m-%dT%H:%M:%S'),
                str(meassurement['temperature']),
            ])
        return cleaned

    def fetchDataFromAllStations(self, days=1, daysAgo=0, weatherType = 'DryBulbTemperature_Celsius'):
        dataFromAllStations = []
        for station in self.stations:
            for i in range(int(station['pages'])):
                startAt = i * 100
                dataFromAllStations.append(self.fetchData(station, days, daysAgo, weatherType, startAt ))

        return dataFromAllStations