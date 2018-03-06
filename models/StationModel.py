from MetWrapper import MetWrapper
class StationModel:

    def __init__(name, longitude, latitude, masl, operational):
        self.name = name
        self.longitude = longitude
        self.latitude = latitude
        self.masl = masl
        self.operational = operational

    def getStationsFromMet():
        stuff = MetWrapper.getStationsFromMet('NO')
        return stuff.json()
