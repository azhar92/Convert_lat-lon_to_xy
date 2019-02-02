#thanks to the internet & Andrea!

%matplotlib notebook

import math
import matplotlib.pyplot as plt
import numpy as np

def calculateBearing(lat1, lon1, lat2, lon2, prevbearing):
    if math.isnan(lat1) or math.isnan(lon1):
        return prevbearing
    if lat1 == lat2 and lon1 == lon2:
        return prevbearing
        # radius = 6371 # km

    rlat1 = math.radians(lat1)
    rlat2 = math.radians(lat2)
    #rlon1 = math.radians(lon1)
    #rlon2 = math.radians(lon2)
    dlon = math.radians(lon2 - lon1)

    b = math.atan2(math.sin(dlon) * math.cos(rlat2), math.cos(rlat1) * math.sin(rlat2) -
                   math.sin(rlat1) * math.cos(rlat2) * math.cos(dlon))  # bearing calc
    bd = math.degrees(b)
    br, bn = divmod(bd + 360, 360)  # the bearing remainder and final bearing
    return bn

def calculateDistance(lat1, lon1, lat2, lon2):
    #distance in meters
    if lat1 == lat2 and lon1 == lon2:
        return 0
    #print lat1, lon1, lat2, lon2,
    rlat1 = math.radians(lat1)
    rlat2 = math.radians(lat2)
    rlon1 = math.radians(lon1)
    rlon2 = math.radians(lon2)

    # radius of earth in metres
    r = 6378137
    d_lat = (rlat2 - rlat1)
    d_long = (rlon2 - rlon1)

    a = math.pow(math.sin(d_lat / 2), 2) + math.cos(rlat1) * math.cos(rlat2) * math.pow(math.sin(d_long / 2), 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    #distance in meters
    return r * c

def convertWGStoXY(lat, lon):
    origin = np.array([1.35430381,103.69662037])
    # for test4.csv = 1.35430381, 103.69662037
    # for test2.2.csv = 1.3545626 , 103.6956862
    # for test3.csv = 1.35425093, 103.69525519
    position = np.array([lat, lon])
    angle = calculateBearing(origin[0], origin[1], position[0], position[1], 0)
    distance = calculateDistance(origin[0], origin[1], position[0], position[1])

    x, y = math.sin(math.radians(angle)) * distance, math.cos(math.radians(angle)) * distance

    return x, y

def convertList(trajectory):
    xyList = list()
    for i in trajectory:
        xyList.append(convertWGStoXY(i[0], i[1]))
    return xyList

def draw(trajectory,c):
    newcoordinates = convertList(trajectory)
    step = 10
    for i in range(len(newcoordinates) - step):
        if i%step == 0:
            x= newcoordinates[i][0], newcoordinates[i+step][0]
            y= newcoordinates[i][1], newcoordinates[i+step][1]
            plt.plot(x,y,color = c)
            
    #plt.show()
    
def readOXTScsv(path):
    latColumnNumeber = 5
    lonColumnNumeber = 6
    trajectory = list()
    with open(path) as f:
        lines = f.readlines()[1:]
        for line in lines:
            words = line.split(',')
            if len(words) > 0:
                lat = words[latColumnNumeber]
                if len(lat) == 0:
                    lat = np.nan
                lon = words[lonColumnNumeber]
                if len(lon) == 0:
                    lon = np.nan
                trajectory.append(np.array([float(lat), float(lon)]))

    return trajectory


#####################################################################################################


#######################################LANE MARKINGS################################################

lane1 = readOXTScsv("lane1.csv")  
lane2 = readOXTScsv("lane2.csv")
lane3 = readOXTScsv("lane3.csv")


####################################################################################################

#trajectory = readOXTScsv("test2.2.csv")
#trajectory1 = readOXTScsv("test3.csv")
#trajectory4 = readOXTScsv("test4.csv")


# #draw(trajectory1)
# draw(trajectory4)
b = 'blue'
r = 'red'

draw(lane1,b)
draw(lane2,b)
draw(lane3,b)

trajectory5 = readOXTScsv("test5.csv")
#trajectory4 = readOXTScsv("test4.csv")
#draw(trajectory1,r)
draw(trajectory5,r)
