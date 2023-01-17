import pandas as pd

from ..db.mongodb import get_database
from ..models.report import ReportBase
from ..analyze.analyze import (
    calculate_basic_stats,
    calculate_basic_stats_of_each_author,
)


async def create_report(document: ReportBase) -> None:
    document = ReportBase(**document).dict()
    await get_database()["reports"].insert_one(document)


async def get_report(chat_id: str) -> dict:
    chat = await get_database()["chats"].find_one(
        {"chat_id": {"$regex": f"{chat_id}$"}}
    )

    if chat is None:
        return None

    df = pd.DataFrame.from_dict(chat["messages"], orient="index")

    results = {
        "basic_stats": calculate_basic_stats(df),
        "basic_stats_of_each_author": calculate_basic_stats_of_each_author(df),
    }

    return results
