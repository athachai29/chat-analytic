from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def root():
    return {"message": "API Version 2 is comming soon..."}
