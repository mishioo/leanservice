from typing import List

from fastapi import APIRouter

from ..schemas import RedditPicture

router = APIRouter()
router.history = []


@router.get("/history", response_model=List[RedditPicture])
async def history():
    return router.history
