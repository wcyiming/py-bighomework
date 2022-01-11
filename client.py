from re import split
import aiohttp
import asyncio
import json
import math
import matplotlib.pyplot as plt
import numpy as np
from numpy.core.fromnumeric import size
from shapely.geometry.polygon import Polygon

async def main():
    n = input("Enter point number:\n")
    print("Enter point(split with ,):\n")
    pointList = []
    for i in range(int(n)):
        tmp = input()
        pointTmp = tmp.split(',')
        x = float(pointTmp[0])
        y = float(pointTmp[1])
        pointList.append((x,y))
    polygonDict = {"type": "Polygon", "coordinates": pointList}
    propertiesDict = {}
    GeoDict = {"type": "Feature",
                "geometry": polygonDict, "properties": propertiesDict}
    messageJson = json.dumps(GeoDict)
    url = 'http://127.0.0.1:8008/populationsmall'

    async with aiohttp.ClientSession() as session:
        async with session.post(url,data = messageJson) as response:
            text = await response.json()
            X1=[]
            Y1=[]
            X2=[]
            Y2=[]
            X3=[]
            Y3=[]
            X4=[]
            Y4=[]
            X5=[]
            Y5=[]     
            for key,value in text.items():
                keystr = str(key)
                if keystr == "Total":
                    titleStr = "Total population is : " + str(value)
                    plt.title(titleStr)
                else:
                    pointNow = keystr.split(",")
                    x = float(pointNow[0])
                    y = float(pointNow[1])
                    valuenum = float(value)
                    if valuenum > 0.0 and valuenum < 100.0:
                        X1.append(x)
                        Y1.append(y)
                    elif valuenum < 10000.0:
                        X2.append(x)
                        Y2.append(y)
                    elif valuenum < 1000000.0:
                        X3.append(x)
                        Y3.append(y)
                    elif valuenum < 10000000.0:
                        X4.append(x)
                        Y4.append(y)
                    else:
                        X5.append(x)
                        Y5.append(y)
            plt.xlim(-180,180)
            plt.ylim(-90, 90)
            plt.scatter(X1, Y1, s = 1, color = '#cde6c7')
            plt.scatter(X2, Y2, s = 1,color = '#1d953f')
            plt.scatter(X3, Y3, s = 1,color = '#4e72b8')
            plt.scatter(X4, Y4, s = 1,color = '#411445')
            plt.scatter(X5, Y5, s = 1,color = '#130c0e')
            plt.xlabel('longtitude')
            plt.ylabel("latitude")
            plt.legend(["0-100","101-10000","10001-1000000","1000001-10000000",">10000000"])
            plt.show()
            

asyncio.run(main())