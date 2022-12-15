from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Union

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


@app.get("/{path:path}", response_class=HTMLResponse)
async def index(request: Request, path: Union[str, None] = None):
    return templates.TemplateResponse(
        "index.html.j2", {"request": request, "path": path}
    )


# @app.get("/upload", response_class=HTMLResponse)
# async def upload(request: Request):
#     return templates.TemplateResponse("upload.html.j2", {"request": request})


# @app.get("/report", response_class=HTMLResponse)
# async def report(request: Request):
#     return templates.TemplateResponse("request_report.html.j2", {"request": request})


# @app.get("/report/{chat_id}", response_class=HTMLResponse)
# async def report(request: Request, chat_id: str):
#     return templates.TemplateResponse(
#         "view_report.html.j2", {"request": request, "chat_id": chat_id}
#     )


# @app.get("/about", response_class=HTMLResponse)
# async def about(request: Request):
#     return templates.TemplateResponse("about.html.j2", {"request": request})


# @app.get("/howto", response_class=HTMLResponse)
# async def about(request: Request):
#     return templates.TemplateResponse("howto.html.j2", {"request": request})
