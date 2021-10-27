from fastapi import FastAPI, File, UploadFile
from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
import extractAvgColor


app = FastAPI()

class color(BaseModel):
    name: str
    code: str
    tone: str
    base: str

class averagecolors(BaseModel):
    color1: Optional[color]
    color2: Optional[color]
    color3: Optional[color]
    color4: Optional[color]


@app.post("/averagecolors")
async def averagecolors(imgfile: UploadFile = File(...)):
    img = await imgfile.read()
    colors = extractAvgColor.extractAvgColor(img)
    return {
        "color1": colors[0],
        "color2": colors[1],
        "color3": colors[2],
        "color4": colors[3]
    }