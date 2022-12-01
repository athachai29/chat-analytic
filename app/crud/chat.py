import json
from pymongo.errors import DuplicateKeyError

from ..db.mongodb import get_database
from ..models.chat import ChatBase
from ..analyze.analyze import parse_data_from_line


async def create_chat(doc: dict) -> None:
    messages = doc["messages"].decode("utf-8").split("\n")
    df_messages = parse_data_from_line(messages)

    doc["messages"] = json.loads(df_messages.T.to_json())
    doc = ChatBase(**doc).dict()

    try:
        await (await get_database())["chats"].insert_one(doc)
    except DuplicateKeyError:
        print("this chat has exists")
    except Exception as e:
        print(e)

    return {"chat_id": doc["chat_id"]}
