from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm.session import Session

from ..crud import get_history
from ..database import get_database
from ..schemas import RedditPicture

router = APIRouter()


@router.get("/history", response_model=List[RedditPicture])
async def history(db: Session = Depends(get_database)):
    """/history endpoint's GET method.
    Returns a JSON representation of all pictures drawn so far.
    """
    return await get_history(db)
