from fastapi import APIRouter

router = APIRouter(prefix="/strategies")


@router.get("/")
async def root():
    return {"message": "Hello World"}