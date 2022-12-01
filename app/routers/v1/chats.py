from fastapi import APIRouter, UploadFile
import uuid
import hashlib

from ...crud.chat import create_chat

router = APIRouter()


@router.post("/", tags=["chats"])
async def create_upload_chats(file: UploadFile):
    content = await file.read()
    hash_object = hashlib.sha1(content)
    chat_id = hash_object.hexdigest()

    results = await create_chat({"chat_id": chat_id, "messages": content})

    return results
