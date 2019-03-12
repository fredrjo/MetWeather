from db import db
import json
from datetime import datetime
from models.station import Station


class Measurement(db.Model):
    __tablename__ = 'measurements'

    id = db.Column(db.Integer, primary_key = True)
    mType = db.Column(db.String(255))
    mtime = db.Column(db.DateTime)
    value = db.Column(db.Float(precision = 2))

    station_id = db.Column(db.Integer, db.ForeignKey("stations.id"))

    def __init__(self, station, mtime, mType, value):
        self.mtime = mtime
        self.mType = mType
        self.value = value
        self.station_id = station

    def saveMany(data):
        for chunk in data:
            for item in chunk['data']:
                for obs in item['observations']:
                    converted = datetime.strptime(item['referenceTime'], '%Y-%m-%dT%H:%M:%S.000Z')
                    myId = Station.getStationIdWithCode(item['sourceId'][0:-2]).id
                    mes = Measurement(myId, converted, obs['elementId'], obs['value'])
                    db.session.add(mes)
        db.session.commit()

    def getDataFrom(station):
        stuff = []

        station = station #+ ':0'
        station_id = Station.findById('Station', station).id
        prepare = Measurement.query.filter_by(station_id=station_id).order_by(Measurement.mtime.asc())
        for item in prepare:
            stuff.append({ 'value' : item.value, 'time' : datetime.strftime(item.mtime , '%Y-%m-%d %H:%M')})
        return stuff

    def getAllDataFromWhere(fromTime, toTime, defType = 'air_temperature'):
        fixThis = []
        returnThis = Measurement.query.filter(Measurement.mtime >= fromTime).filter(Measurement.mtime <= toTime).filter(Measurement.mType==defType).all()
        for mes in returnThis:
            print(mes)
            #fixThis.append({'station': mes.station , 'value' : mes.value, 'time': datetime.strftime(mes.mtime, '%Y-%m-%dT%H:%M:%S.000Z')})
            fixThis.append({'station': Station.findById('Station', mes.station_id).code , 'value' : mes.value, 'time': datetime.strftime(mes.mtime, '%Y-%m-%d %H:%M:%S.000Z')})

        return fixThis
