import requests
import json
import datetime
import os.path
import sys

def run(days, daysAgo, spesific_station):
    #surl = "http://fredrik.cebyc.int:5300/stations"
    # surl = "http://localhost:5300/stations"
    #res = requests.get(surl)
    #print(res.text)
    stations = [spesific_station]
    url = "http://loke.cebyc.int:5300/report?days="+days+"&daysAgo="+daysAgo
    #url = "http://localhost:5300/report?days="+days+"&daysAgo="+daysAgo
    response = requests.get(url)
    data = response.json()
    finaldata = []
    print(stations)
    print(data)
    for station in data:
        station_code = station['station']
        stationname = stations[station_code]
        humandate = station['time']
        finaldata.append(';'.join([station_code[2:],  stationname, humandate, str(station['value'])]))
    else:
        print(stations)

    print(finaldata)
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
        spesific_station = sys.argv[3]
    run(days, daysAgo, spesific_station)