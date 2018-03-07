import sqlite3
import json
from db import db

from MetWrapper import MetWrapper
class StationModel(db.Model):
    __tablename__ = 'stations'

    id = db.Column(db.String, primary_key = True)
    name = db.Column(db.String(255))

    def __init__(self, id, name): #, longitude, latitude, masl, operational):
        self.id = id
        self.name = name
        #self.longitude = longitude
        #self.latitude = latitude
        #self.masl = masl
        #self.operational = operational

    def findByName(cls, name):
        return cls.query.filter_by(name=name).first()

    def getAllStations(cls):
        stations = []
        getThemBoiz = StationModel.query.all()
        for st in getThemBoiz:
            stations.append({'id' : st.id, 'name' : st.name})
        return stations


    def getStationsFromMet():
        stuff = MetWrapper.getStationsFromMet('NO')
        #print(stuff)
        for item in stuff['data']:
            print(item)
            newStation = StationModel(item['id'], item['name'])
            db.session.add(newStation)
        db.session.commit()
#        print('ok')
