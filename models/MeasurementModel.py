from db import db

class MeasurementModel(db.Model):
    __tablename__ = 'measurements'
    id = db.Column(db.Integer, primary_key = True)
    mType = db.Column(db.String(255))
    value = db.Column(db.Float(precision = 2))
    station = db.Column(db.String(255), db.ForeignKey("stations.id"))

    def __init__(self, station, dateTime, mType, value):
        self.dateTime = dateTime
        self.mType = mType
        self.value = value
        self.station = station

    def saveMany(data):
        print(data['data'][0])
        for item in data['data']:
            for obs in item['observations']:
                mes = MeasurementModel('SN18700', item['referenceTime'], obs['elementId'], obs['value'])
                db.session.add(mes)

        db.session.commit()

    def getDataFrom(station):
        return MeasurementModel.query.filter_by(station=station).first()
