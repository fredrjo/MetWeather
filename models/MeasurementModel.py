from db import db
import json
from datetime import datetime

class MeasurementModel(db.Model):
    __tablename__ = 'measurements'
    id = db.Column(db.Integer, primary_key = True)
    mType = db.Column(db.String(255))
    mtime = db.Column(db.DateTime)
    value = db.Column(db.Float(precision = 2))
    station = db.Column(db.String(255), db.ForeignKey("stations.id"))

    def __init__(self, station, mtime, mType, value):
        self.mtime = mtime
        self.mType = mType
        self.value = value
        self.station = station

    def saveMany(data):
        for chunk in data:
            for item in chunk['data']:
                for obs in item['observations']:
                    converted = datetime.strptime(item['referenceTime'], '%Y-%m-%dT%H:%M:%S.000Z')
                    if (MeasurementModel.query.filter_by(station=item['sourceId'][0:-2], mtime=converted, mType=obs['elementId']).first()==None):
                        mes = MeasurementModel(item['sourceId'][0:-2], converted, obs['elementId'], obs['value'])
                        db.session.add(mes)
        db.session.commit()

    def getDataFrom(station):
        stuff = []

        station = station #+ ':0'
        prepare = MeasurementModel.query.filter_by(station=station).order_by(MeasurementModel.mtime.asc())
        for item in prepare:
            stuff.append({ 'value' : item.value, 'time' : datetime.strftime(item.mtime , '%Y-%m-%d %H:%M')})
        return stuff

    def getAllDataFromWhere(fromTime, toTime, defType = 'air_temperature'):
        fixThis = []
        returnThis = MeasurementModel.query.filter(MeasurementModel.mtime >= fromTime).filter(MeasurementModel.mtime <= toTime).filter(MeasurementModel.mType==defType).all()
        for mes in returnThis:
            #fixThis.append({'station': mes.station , 'value' : mes.value, 'time': datetime.strftime(mes.mtime, '%Y-%m-%dT%H:%M:%S.000Z')})
            fixThis.append({'station': mes.station , 'value' : mes.value, 'time': datetime.strftime(mes.mtime, '%Y-%m-%d %H:%M')})

        return fixThis
