from fastapi import Depends, APIRouter, Request
from app.library.security import check_authenticated
from app.library.logging import log_usage
from app.database.database_init import get_log_session
from sqlalchemy.orm import Session
from app.data_mappers.data_mappers import User

# API instanciation
router = APIRouter(
    tags=["API state"],
    responses = {401: {"description": "Not authenticated"}, 404: {"description": "Not found"}},
)

@router.get('/status', description="Return 1 if API is OK")
async def get_status(   request : Request, 
                        db: Session = Depends(get_log_session), 
                        user: User = Depends(check_authenticated)):
    log_usage(db, user.id, request)
    return "1"