from gpx_converter import Converter
from math import radians, cos, sin, asin, sqrt
import os

fpath = "GPX/"

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance in kilometers between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles. Determines return value units.
    return c * r

#array of files to read in
def fname(fpath):
    file_list = os.listdir(fpath)
    #print("File List: {0}".format(file_list))
    return file_list

def MaxiMini(distToEle):
    mod = 100
    MaxMinArray = []
    #get maximum and minimum elevation
    maxi = distToEle[max(distToEle.keys(), key=(lambda k: distToEle[k]))]
    mini = distToEle[min(distToEle.keys(), key=(lambda k: distToEle[k]))]
    MaxMinArray.append(round(mini-mini%mod))
    MaxMinArray.append(round(maxi+maxi%mod))
    print('Maximum Plot Elevation: ', MaxMinArray[0])
    print('Minimum Plot Elevation: ', MaxMinArray[1])
    #print('Maximum Plot Distance: ', MaxMinArray[2])

    return MaxMinArray

def gpxElevationPlotGen(gpxFile):
    """
    Turns any GPX file into a
    """
    print(gpxFile)
    np_array = Converter(gpxFile).gpx_to_numpy_array()
    #print(np_array)
    dist = 0
    html = {}
    html[dist] = np_array[0][3]

    for n in range(0, len(np_array)-1):
        dist += haversine(np_array[n][1], np_array[n][2], np_array[n+1][1], np_array[n+1][2])
        html[dist] = np_array[n+1][3]

    MaxMinArray = MaxiMini(html)
    with open("elevationPlot.txt", "r") as f:
        contents = f.readlines()

    data = "\t\t  data: {0},\n".format(html)
    #max Distance
    elev = "\t\t\t\t\tmax: {0},\n \t\t\t\t\tmin: {1},\n".format(MaxMinArray[0], MaxMinArray[1])

    contents.insert(13, data)
    contents.insert(40, elev)
    folder = gpxFile.find(fpath) + len(fpath)
    ext = gpxFile.find('gpx', folder)
    htmlFile = gpxFile[folder:ext] + "html"
    print(htmlFile)
    with open(htmlFile, "w") as f:
        contents = "".join(contents)
        f.write(contents)

file_list = fname(fpath)
for file in file_list:
    gpxElevationPlotGen(fpath + file)
