from fastapi import APIRouter

router = APIRouter()


@router.post("/room/{room_id}")
async def room(room_id: int) -> None:
    