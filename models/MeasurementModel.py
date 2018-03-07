from db import db

class MeasurementModel(db.Model):
    __tablename__ = 'measurements'
    id = db.Column(db.Integer, primary_key = True)
    mType = db.Column(db.String(255))
    value = db.Column(db.Float(precision = 2))

    def __init__(self, dateTime, mType, value):
        self.dateTime = dateTime
        self.mType = mType
        self.value = value
