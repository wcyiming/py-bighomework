from sanic import Sanic
from sanic import response
import json
import numpy as np
from shapely import geometry

from sanic.signals import RESERVED_NAMESPACES

app = Sanic("Population Program")

testPath = 'D:\\programs\\py\\py-f\\data.asc'
testPath2 = 'D:\\programs\\py\\py-f\\datab.asc'
data = []


@app.route("/populationbig", methods=["POST",])
async def populationbig(request):
    initbig()
    pointList = request.json["geometry"]["coordinates"]
    ansDict = calcPopulations(pointList)
    JsonArray = json.dumps(ansDict)
    print(ansDict)
    return response.json(JsonArray)

def initbig():
    file = open(testPath)
    lines = file.readlines()
    for line in lines:
        line = line.replace("\n","")
        data.append(line.split(" "))

def getPolulationFromFileb(cellLon1, cellLat1):
    i = -(cellLat1 - 90) * 3600 / 30
    j = (cellLon1 + 180) * 3600 / 30
    return data[i][j]

def calcPopulationb(lonLats):
    answerDict = {}
    polygon = geometry.Polygon(lonLats)
    lonMin, latMin,lonMax,latMax = polygon.bounds
    step = 30 / 3600
    cellArea = geometry.Polygon(0, 0, step, step).area
    populationTotal = 0
    for lon in np.arange(lonMin, lonMax, step):
        for lat in np.arange(latMin, latMax, step):
            cellLon1 = lon - lon % step - step
            cellLon2 = lon - lon % step + step
            cellLat1 = lat - lat % step - step
            cellLat2 = lat - lat % step + step
            cellPolygon = geometry.Polygon(cellLon1, cellLat1, cellLon2, cellLat2)
            area = cellPolygon.intersection(polygon).area
            if area > 0.0:
                p = getPolulationFromFileb(cellLon1, cellLat1)
                populationTotal += (area / cellArea) * p;
                var1 = str(cellLon1)
                var2 = str(cellLat1)
                var3 = var1 + "," + var2
                answerDict[var3] = (area / cellArea) * p
    answerDict['Total'] = populationTotal
    return answerDict

@app.route("/populationsmall", methods=["POST",])
async def populationsmall(request):
    initSmall()
#    print(request)
    pointList = request.json["geometry"]["coordinates"]
    ansDict = calcPopulations(pointList)
    print(ansDict)
    return response.json(ansDict)

def initSmall():
    file = open(testPath)
    lines = file.readlines()
    for line in lines:
        line = line.replace("\n","")
        data.append(line.split(" "))

def getPolulationFromFiles(cellLon1, cellLat1):
    i = int(-(cellLat1 - 90) * 1)
    j = int((cellLon1 + 180) * 1)
    return float(data[i][j])


def calcPopulations(lonLats):
    answerDict = {}
    polygon = geometry.Polygon(lonLats)
    lonMin, latMin,lonMax,latMax = polygon.bounds
    step = 1
    cellArea = geometry.box(0, 0, step, step).area
    populationTotal = 0
    for lon in np.arange(lonMin, lonMax, step):
        for lat in np.arange(latMin, latMax, step):
            cellLon1 = lon - lon % step - step
            cellLon2 = lon - lon % step + step
            cellLat1 = lat - lat % step - step
            cellLat2 = lat - lat % step + step
            cellPolygon = geometry.box(cellLon1, cellLat1, cellLon2, cellLat2)
            area = cellPolygon.intersection(polygon).area
            if area > 0.0:
                p = getPolulationFromFiles(cellLon1, cellLat1)
                populationTotal += (area / cellArea) * p;
                var1 = str(cellLon1)
                var2 = str(cellLat1)
                var3 = var1 + "," + var2
                answerDict[var3] = (area / cellArea) * p
    answerDict['Total'] = populationTotal
    return answerDict


@app.route("/")
async def test(request):    
    return response.json({"hello": "world"})

if __name__ == "__main__":

    app.run(host="127.0.0.1", port=8008)

    #http://127.0.0.1:8000/search?start=1900&end=2000&cmp=up&form=CSV