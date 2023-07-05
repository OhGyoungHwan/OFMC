from pymongo import MongoClient

client = MongoClient("localhost", 27017)
db = client["coloravg"]
coll = db["color"]


def similarColor(base):
    if base == "red":
        return ["purple", "orange", "red"]
    elif base == "orange":
        return ["red", "yellow", "orange"]
    elif base == "yellow":
        return ["orange", "green", "yellow"]
    elif base == "green":
        return ["yellow", "blue", "green"]
    elif base == "blue":
        return ["green", "purple", "blue"]
    elif base == "purple":
        return ["blue", "red", "purple"]
    elif base == "white":
        return ["white"]
    elif base == "gray":
        return ["gray"]
    elif base == "black":
        return ["black"]


def complementaryColor(base):
    if base == "red":
        return ["green"]
    elif base == "orange":
        return ["blue"]
    elif base == "yellow":
        return ["purple"]
    elif base == "green":
        return ["red"]
    elif base == "blue":
        return ["orange"]
    elif base == "purple":
        return ["yellow"]
    elif base == "white":
        return ["black"]
    elif base == "gray":
        return ["gray"]
    elif base == "black":
        return ["white"]


def triColor(base):
    if base == "red":
        return ["yellow", "blue"]
    elif base == "orange":
        return ["green", "purple"]
    elif base == "yellow":
        return ["blue", "red"]
    elif base == "green":
        return ["orange", "purple"]
    elif base == "blue":
        return ["yellow", "red"]
    elif base == "purple":
        return ["orange", "green"]
    elif base == "white":
        return ["white"]
    elif base == "gray":
        return ["gray"]
    elif base == "black":
        return ["black"]


def similarTone(tone):
    if tone == "b":
        return ["s", "b"]
    elif tone == "d":
        return ["sf", "dk", "d"]
    elif tone == "dk":
        return ["d", "dk"]
    elif tone == "dkg":
        return ["g", "dkg"]
    elif tone == "dp":
        return ["s", "dp"]
    elif tone == "g":
        return ["ltg", "dkg", "g"]
    elif tone == "lf":
        return ["sf", "lf"]
    elif tone == "ltg":
        return ["p", "g", "ltg"]
    elif tone == "p":
        return ["ltg", "p"]
    elif tone == "s":
        return ["b", "dp", "s"]
    elif tone == "sf":
        return ["lf", "d", "sf"]
    elif tone == "v":
        return ["b", "dp", "v"]


def complementaryTone(tone):
    if tone == "b":
        return ["dk"]
    elif tone == "d":
        return ["v"]
    elif tone == "dk":
        return ["v"]
    elif tone == "dkg":
        return ["v"]
    elif tone == "dp":
        return ["p"]
    elif tone == "g":
        return ["b"]
    elif tone == "lf":
        return ["v"]
    elif tone == "ltg":
        return ["v"]
    elif tone == "p":
        return ["dp"]
    elif tone == "s":
        return ["dkg"]
    elif tone == "sf":
        return ["v"]
    elif tone == "v":
        return ["dkg"]


def extractStyleColor(style, base, tone):
    ptone = []
    pcolor = []
    returnRGB = []
    for pstyle in style:
        if style == "minimum":
            ptone += similarTone(tone)
            pcolor += similarColor(base)
            pcolor.append("white")

        elif style == "lovely":
            ptone += similarTone(tone)
            pcolor += similarColor(base)

        elif style == "natural":
            ptone += similarTone(tone)
            pcolor += triColor(base)

        elif style == "casual":
            ptone += similarTone(tone)
            pcolor += complementaryColor(base)
            pcolor.append("white")

        elif style == "classic":
            ptone += similarTone(tone)
            pcolor += similarColor(base)
            pcolor.append("black")
            pcolor.append("gray")

        elif style == "elegant":
            ptone += similarTone(tone)
            ptone.remove(tone)
            pcolor += similarColor(base)
            pcolor.remove(base)
            pcolor.append("gray")

        elif style == "modern":
            ptone += [tone]
            pcolor += [base]
            pcolor.append("white")
            pcolor.append("gray")
            pcolor.append("black")

        elif style == "ethnic":
            ptone += complementaryTone(tone)
            pcolor += triColor(base)

        elif style == "rockchic":
            ptone += ["b", "d", "dk", "dkg", "dp",
                      "g", "lf", "ltg", "p", "s", "sf", "v"]
            pcolor += ["black"]

        elif style == "amekaji":
            ptone += tone
            pcolor += similarColor(base)

        elif style == "retro":
            ptone += similarTone(tone)
            pcolor += similarColor(base)

        elif style == "toneintone":
            ptone += [tone]
            pcolor += ["red", "orange", "yellow", "green", "blue", "purple"]
            pcolor.remove(base)

        elif style == "toneontone":
            ptone += similarTone(tone)
            pcolor += [base]

    for i in coll.find({"tone": {'$in': ptone}, "base": {'$in': pcolor}}):
        returnRGB.append(i["RGB"])

    return returnRGB
