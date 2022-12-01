from fastapi import APIRouter

from .chats import router as chats_router
from .reports import router as reports_router

router = APIRouter()
router.include_router(chats_router)
router.include_router(reports_router)


@router.get("/")
async def root():
    return {"message": "API Version 1"}
