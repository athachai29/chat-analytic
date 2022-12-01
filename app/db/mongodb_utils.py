from motor.motor_asyncio import AsyncIOMotorClient

from .mongodb import db
from .. import config


async def connect_to_mongo():
    db.client = AsyncIOMotorClient(config.Settings().db_url)


async def close_mongo_connection():
    db.client.close()
