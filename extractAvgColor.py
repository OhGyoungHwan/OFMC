from sklearn.cluster import KMeans
import numpy as np
import cv2
import math
import pandas as pd


NUMBER_OF_COLORS = 6
DF_MIN = 1000


color = pd.read_csv("csv/colors.csv")


def closecolor(x, y, z):
    global color
    minimumdifference = DF_MIN
    minimumdifferenceindex = 0
    for colorindex in range(len(color)):
        currentdifference = math.sqrt(
            (x-color["x"][colorindex])**2 +
            (y-color["y"][colorindex])**2 +
            (z-color["z"][colorindex])**2
        )
        if minimumdifference > currentdifference:
            minimumdifference = currentdifference
            minimumdifferenceindex = colorindex
    print(color["name"][minimumdifferenceindex])
    return {
        "name": color["name"][minimumdifferenceindex],
        "code": color["RGB"][minimumdifferenceindex],
        "tone": color["tone"][minimumdifferenceindex],
        "base": color["base"][minimumdifferenceindex]
    }


def hsvtoxyz(h, s, v):
    x = s*math.cos(2*math.pi*h/255)*v/255
    y = s*math.sin(2*math.pi*h/255)*v/255
    z = v
    return x, y, z


def bgrtohsv(bgr):
    bgr[0] = bgr[0]/255.0
    bgr[1] = bgr[1]/255.0
    bgr[2] = bgr[2]/255.0
    v = max(bgr)
    m = min(bgr)
    if v == 0:
        s = 0
        h = 0
    else:
        s = 1 - m/v
        if bgr[0] == bgr[1] and bgr[1] == bgr[2]:
            h = 0
        elif v == bgr[2]:
            h = 60 * (bgr[1] - bgr[0]) / (v - m)
        elif v == bgr[1]:
            h = 120 + (60 * (bgr[0] - bgr[2])) / (v - m)
        elif v == bgr[0]:
            h = 240 + (60 * (bgr[2] - bgr[1])) / (v - m)
        if h < 0:
            h += 360
        h /= 360
        h *= 255
    s = s*255
    v = v*255

    return h, s, v


def extractAvgColor(img):
    colorlistall = []
    onedimensionimg = np.frombuffer(img, dtype=np.uint8)
    threedimensionimage = cv2.imdecode(onedimensionimg, cv2.IMREAD_COLOR)
    smallthreedimensionimage = cv2.resize(
        threedimensionimage, dsize=(640, 480), interpolation=cv2.INTER_AREA
    )
    onelinecolors = smallthreedimensionimage.reshape(
        (smallthreedimensionimage.shape[0] *
         smallthreedimensionimage.shape[1],
         3)
    )
    clt = KMeans(n_clusters=NUMBER_OF_COLORS)
    clt.fit(onelinecolors)
    for bgr in clt.cluster_centers_:
        h, s, v = bgrtohsv(bgr)
        x, y, z = hsvtoxyz(h, s, v)
        colorlistall.append(closecolor(x, y, z))
    return colorlistall
