from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# from pydantic import BaseModel

from .db.mongodb_utils import close_mongo_connection, connect_to_mongo

# from .db.mongodb import AsyncIOMotorClient, get_database

from .routers.v1 import router as api_router_v1
from . import config

# from .routers.v2 import router as api_router_v2

app = FastAPI(
    title=config.Settings().fastapi_title,
    description=config.Settings().fastapi_description,
    contact={
        "name": config.Settings().fastapi_contact_name,
        "url": config.Settings().fastapi_contact_url,
        "email": config.Settings().fastapi_contact_email,
    },
    license_info={
        "name": config.Settings().fastapi_license_info_name,
        "url": config.Settings().fastapi_contact_url,
    },
)

# manage db connection
app.add_event_handler("startup", connect_to_mongo)
app.add_event_handler("shutdown", close_mongo_connection)

templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")


app.include_router(api_router_v1, prefix="/api")
# app.include_router(api_router_v2, prefix="/api/v2")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
