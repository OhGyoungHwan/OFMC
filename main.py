from fastapi import FastAPI, Request, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Optional
from pydantic import BaseModel
import extractAvgColor


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


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


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/averagecolors")
async def averagecolor(file: UploadFile = File(...)):
    img = await file.read()
    colors = extractAvgColor.extractAvgColor(img)
    return {
        "color1": colors[0],
        "color2": colors[1],
        "color3": colors[2],
        "color4": colors[3]
    }
