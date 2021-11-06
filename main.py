from fastapi import FastAPI, Request, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.encoders import jsonable_encoder
from typing import Optional
from pydantic import BaseModel, Field
from pymongo import MongoClient
from bson import ObjectId
import extractAvgColor
import extractStyleColor


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

client = MongoClient("localhost", 27017)
db = client["coloravg"]


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


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


class pickcolor(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str
    h: int
    s: int
    v: int
    x: float
    y: float
    z: int
    tone: str
    base: str
    RGB: str

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "흰색",
                "h": "0",
                "s": "0",
                "v": "225",
                "x": "0",
                "y": "0",
                "z": "225",
                "tone": "p",
                "base": "white",
                "RGB": "FFFFFF",
            }
        }


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/recommendstyle/{colorcode}")
async def read_user_item(colorcode: str):
    extractioncolor = {}
    explanationstyle = {}
    coll = db["color"]
    color = coll.find_one({'RGB': colorcode})
    tone = color['tone']
    base = color['base']
    coll = db["colors_recommend_styles"]
    style = coll.find_one({'tone': tone, 'base': base})['style'].split(", ")

    if (base != "white" and base != "gray") and base != "black":
        style += ["toneontone", "toneintone"]
    elif base == "gray":
        style += ["toneontone"]

    for i in style:
        colors = extractStyleColor.extractStyleColor(i, base, tone)
        extractioncolor[i] = colors

    coll = db["styles"]
    for i in style:
        explanation = coll.find_one({'name': i})['exp']
        explanationstyle[i+"explanation"] = explanation
    return {
        "extractioncolor": extractioncolor,
        "explanationstyle": explanationstyle
    }


@app.post("/averagecolors", status_code=200)
async def averagecolor(file: UploadFile = File(...)):
    img = await file.read()
    colors = extractAvgColor.extractAvgColor(img)
    return {
        "color1": colors[0],
        "color2": colors[1],
        "color3": colors[2],
        "color4": colors[3],
        "color5": colors[4],
        "color6": colors[5]
    }
