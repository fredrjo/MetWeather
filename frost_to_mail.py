import requests
import json
import datetime
import os.path
import sys
from frostweather import Frostweather

def run(days, daysAgo):
    weather = Frostweather()
    finaldata = []
    data = weather.fetchDataFromAllStations(int(days), int(daysAgo))
    for station in data:
        for meass in station:
            finaldata.append(';'.join(meass))

    useDatedate = datetime.datetime.now() - datetime.timedelta(int(daysAgo))
    date = useDatedate.strftime('%Y-%m-%d')
    fname = 'data/met' + date + '.txt'
    if not os.path.isfile(fname):
        # create file, add header
        file = open(fname, 'w+')
        file.write("###################################################\n")
        file.write("## Timesverdier fra Met\n")
        file.write("##\n")
        file.write("## Dato : %s\n" % date)
        file.write("## Prefix : met\n")
        file.write("##\n")
        file.write("## Stasjonid, stasjonnavn, timestamp, timestemperatur\n")
        file.write("##\n")
        file.close()
        print(finaldata)
    with open(fname, "a", encoding="utf-8") as addfile:
        for line in finaldata:
            line = line + str('\n')
            addfile.write(line)

if __name__ == '__main__': 
    days = "1"
    daysAgo = "0"
    if (len(sys.argv)>1):
        days = sys.argv[1]
        daysAgo = sys.argv[2]
    run(days, daysAgo)