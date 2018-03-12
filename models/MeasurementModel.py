from db import db
import json

class MeasurementModel(db.Model):
    __tablename__ = 'measurements'
    id = db.Column(db.Integer, primary_key = True)
    mType = db.Column(db.String(255))
    mtime = db.Column(db.String(24))
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
                    mes = MeasurementModel(item['sourceId'], item['referenceTime'], obs['elementId'], obs['value'])
                    db.session.add(mes)

        db.session.commit()

    def getDataFrom(station):
        stuff = []
        station = station + ':0'
        prepare = MeasurementModel.query.filter_by(station=station)
        #print(len(prepare))
        for item in prepare:
            stuff.append(item.value)
        return stuff
