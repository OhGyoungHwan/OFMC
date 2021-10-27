from sklearn.cluster import KMeans
import numpy as np
import cv2
import math
import pandas as pd


NUMBER_OF_COLORS = 4
DF_MIN = 1000


color = pd.read_csv("csv/colors.csv")
analysis = pd.read_csv("csv/Analysis.csv", index_col=0)


def f_Analysis(base, tone, sex, tob):
    print(tone, base)
    string = analysis[tone][base]
    listcolor = color[(color['tone'] == tone) & (color['base'] == base)]
    listcolor = listcolor[['name']].values.tolist()
    print(listcolor)
    Explanation = string.split('\n\n')
    Explanation_renew = []
    style_img = []
    for i in range(len(Explanation[2:])):
        if "Clear" in Explanation[2+i]:
            style_img.append("clear.")
        elif "Active" in Explanation[2+i]:
            style_img.append("active.")
        elif "Casual" in Explanation[2+i]:
            style_img.append("casual.")
        elif "Classic" in Explanation[2+i]:
            style_img.append("classic.")
        elif "Elegant" in Explanation[2+i]:
            style_img.append("elegant.")
        elif "Ethnic" in Explanation[2+i]:
            style_img.append("Ethnic.")
        elif "Modern" in Explanation[2+i]:
            style_img.append("modern.")
        elif "Natural" in Explanation[2+i]:
            style_img.append("natural.")
        elif "Tender" in Explanation[2+i]:
            style_img.append("tender.")
        Explanation_renew.append(Explanation[2+i])
        print(Explanation_renew[i])
        print(style_img)
    Explanation_dit = {
        "base": Explanation[0].replace('\n', '<br>'),
        "shape": Explanation[1].replace('\n', '<br><br>'),
        "style": Explanation_renew,
        "img": style_img,
        "color": listcolor
    }
    return Explanation_dit


def closecolor(x, y, z):
    minimumdifference = DF_MIN
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
            if v == bgr[2]:
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
    #모든 평균색의 정보를 담을 공간
    onedimensionimg = np.frombuffer(img, dtype = np.uint8)
    threedimensionimage = cv2.imdecode(onedimensionimg, cv2.IMREAD_COLOR)
    smallthreedimensionimage = cv2.resize(threedimensionimage, dsize=(640, 480), interpolation=cv2.INTER_AREA)
    #image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    onelinecolors = smallthreedimensionimage.reshape((smallthreedimensionimage.shape[0] * smallthreedimensionimage.shape[1], 3)) 
    #HSV이미지를 색상의 한줄 조합으로 가져오는 부분
    clt = KMeans(n_clusters=NUMBER_OF_COLORS)
    clt.fit(onelinecolors)
    for bgr in clt.cluster_centers_:
        h, s, v = bgrtohsv(bgr)
        x, y, z = hsvtoxyz(h, s, v)
        colorlistall.append(closecolor(x, y, z))
    return colorlistall