import requests
import json
import datetime
import os.path

def run():
    url = "http://fredrik.cebyc.int:5300/report?days=1"
    response = requests.get(url)
    data = response.json()
    finaldata = []
    for station in data:
        print(station)
        stationid = station['station'][2:]
        stationname = 'Nordpolen'
        humandate = station['time']
        finaldata.append(';'.join([stationid, stationname, humandate, str(station['value'])]))
    else:
        print(station)

    date = datetime.datetime.now().strftime('%Y-%m-%d')
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

    with open(fname, "a", encoding="utf-8") as addfile:
        for line in finaldata:
            line = line + str('\n')
            addfile.write(line)

if __name__ == '__main__':
    run()
