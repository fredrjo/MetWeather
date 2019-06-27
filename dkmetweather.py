import datetime

import sys, os
import requests
import dateutil.parser as dp
import json
from bs4 import BeautifulSoup

class Dkmetweather:

    url = 'https://wow.metoffice.gov.uk/observations/details/tableview/'
    stationsFile = 'resources/dk_met_stations.json'
    dateFormat = '%Y-%m-%d %H:%M'

    stations = []

    def __init__(self):
         self.setStations()

    def setStations(self):
        data = []
        with open(self.stationsFile) as json_file:  
            data = json.load(json_file)
        for station in data['stations']:
            self.stations.append(station)

    def getGetParameters(self, days, daysAgo, weatherType):
        fromDay = datetime.date.today() - datetime.timedelta(days=daysAgo + days)
        toDay = datetime.date.today() - datetime.timedelta(days=daysAgo)
        return '/details/{}?startAt=0&hours=23:59:59&firstDate={}&lastDate={}&fields={}'.format(
            fromDay.strftime('%Y-%m-%d'),
            fromDay.strftime('%Y-%m-%d'),
            toDay.strftime('%Y-%m-%d'),
            weatherType
        )

    def fetchData(self, station, days, daysAgo, weatherType):
        page = requests.get(self.url + station['id'] + self.getGetParameters(days, daysAgo, weatherType))
        soup = BeautifulSoup(page.text, 'html.parser')
        closer = soup.findAll("tr")
        lol = []
        for item in closer:
            temp = item.findAll('td')
            if len(temp) > 2:
                lol.append({'time' : temp[0].text, 'temperature' : temp[1].text})
        return self.cleanDataFromWow(lol, station)

    def rearrangeDate(self, theDate, inFormat):
        temp = datetime.datetime.strptime(theDate, inFormat)
        return temp.strftime(self.dateFormat)

    def cleanDataFromWow(self, jsondata, station):
        cleaned = []
        for meassurement in jsondata:
            cleaned.append([
                station['id'],
                station['name'],
                self.rearrangeDate(str(meassurement['time']), '%d/%m/%Y %H:%M:%S'),
                str(meassurement['temperature']),
            ])
        return cleaned

    def fetchDataFromAllStations(self, days=1, daysAgo=0, weatherType = 'DryBulbTemperature_Celsius'):
        dataFromAllStations = []
        for station in self.stations:
            dataFromAllStations.append(self.fetchData(station, days, daysAgo, weatherType ))

        return dataFromAllStations

