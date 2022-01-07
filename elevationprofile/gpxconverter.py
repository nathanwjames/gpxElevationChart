from gpx_converter import Converter
from math import radians, cos, sin, asin, sqrt
import os, json

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
def fname():
    file_list = os.listdir(r)
    print(file_list)

def MaxiMini(distToEle):
    MaxMinArray [3] = 0
    maxi = html[max(html.keys(), key=(lambda k: html[k]))]
    mini = html[min(html.keys(), key=(lambda k: html[k]))]
    MaxMinArray[0] = round(mini-mini%mod)
    MaxMinArray[1] = round(maxi+maxi%mod)

    print('Maximum Plot Elevation: ', MaxMinArray[0])
    print('Minimum Plot Elevation: ', MaxMinArray[1])
    print('Maximum Plot Distance: ', MaxMinArray[2])

    return MaxMinArray

for file in file_list:
    np_array = Converter(input_file='BallHut.gpx').gpx_to_numpy_array()
    dist = 0
    #mod = 100
    html = {}
    html[dist] = np_array[0][3]

    for n in range(0, len(np_array)-1):
        dist += haversine(np_array[n][1], np_array[n][2], np_array[n+1][1], np_array[n+1][2])
        html[dist] = np_array[n+1][3]

    MaxMinArray = MaxiMini(html)
    with open("elevationPlot.txt", "r") as f: #change to html instead of txt
        contents = f.readlines()

    data = "\t\t  data: {0},\n".format(html)
    #max Distance
    elev = "\t\t\t\t\tmax: {0},\n \t\t\t\t\tmin: {1},\n".format(MaxMinArray[0], MaxMinArray[1])

    contents.insert(13, data)
    contents.insert(40, elev)


    with open("BallHut.html", "w") as f:
        contents = "".join(contents)
        f.write(contents)
