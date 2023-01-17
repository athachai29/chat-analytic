from motor.motor_asyncio import AsyncIOMotorClient

from .mongodb import db
from .. import config


def connect_to_mongo():
    db.client = AsyncIOMotorClient(config.Settings().db_url)


def close_mongo_connection():
    db.client.close()
