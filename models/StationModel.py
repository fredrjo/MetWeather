import sqlite3
import json
from db import db

from MetWrapper import MetWrapper

class StationModel(db.Model):
    __tablename__ = 'stations'

    id = db.Column(db.String, primary_key = True)
    name = db.Column(db.String(255))
    masl = db.Column(db.String(255)) #meter above sea level
    hasHourTemp = db.Column(db.Boolean)


    def __init__(self, id, name, masl, hourly): #, longitude, latitude, masl, operational):
        self.id = id
        self.name = name
        #self.longitude = longitude
        #self.latitude = latitude
        self.masl = masl
        self.hasHourTemp = hourly
        #self.operational = operational

    def findByName(cls, name):
        return cls.query.filter_by(id=name).first()

    def getAllStations(cls):
        stations = []
        getThemBoiz = cls.query.filter_by(hasHourTemp=True)
        for st in getThemBoiz:
            stations.append({'id' : st.id, 'name' : st.name, 'masl': st.masl})
        return stations

    def getOperational():
        operational = []
        theseHaveHourTemp = MetWrapper.getStationsWithElementAndResolution('air_temperature', 'PT1H')
        for station in theseHaveHourTemp['data']:
            #operational.append(station)
            operational.append(station['sourceId'][0:-2])
        return operational

    def getAllStationsAsString(cls):
        stations = []
        getThemBoiz = cls.query.filter_by(hasHourTemp=True)
        for st in getThemBoiz:
            stations.append(st.id)
        return stations

    def getStationOptions(id):
        stuff = MetWrapper.getOptionsFromMet(id)
        return stuff

    def getStationsFromMet():
        stuff = MetWrapper.getStationsFromMet('NO')
        return stuff        #print(stuff)
        for item in stuff['data']:
            print(item)
            if 'geometry' in item:
                print(item['geometry'])
                #newStation = StationModel(item['id'], item['name'], ' '.join(str(e) for e in item['geometry']['coordinates']));
                #db.session.add(newStation)

        #db.session.commit()
#        print('ok')
    def saveManyStaions(stationList):
        for item in stationList:
            if 'geometry' in item:
                newStation = StationModel(item['id'], item['name'], ' '.join(str(e) for e in item['geometry']['coordinates']), item['hasHourTemp']);
                db.session.add(newStation)
        db.session.commit()
