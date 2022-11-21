from datetime import datetime
from fastapi import Depends, HTTPException, status, APIRouter, Request
from pydantic import BaseModel
from app.database.database_init import get_log_session
from sqlalchemy.orm import Session
from app.data_mappers import data_mappers as db_model
from app.library.security import check_is_admin
from app.data_mappers.data_mappers import User
from app.library.logging import log_usage

# API instanciation

router = APIRouter(
    tags=["Logs"],
    responses={401: {"description": "Not authorized"}}
)

# Pydantic model

class UsageLog(BaseModel):
    id : int
    time_stamp : datetime
    userid : int
    api_route : str
    class Config:
        orm_mode = True

# Return log entries most recent first with pagination

@router.get("/usage_logs", response_model=list[UsageLog])
async def get_usage_logs(   request : Request, 
                            skip: int = 0, limit: int = 100, 
                            db: Session = Depends(get_log_session), 
                            user: User = Depends(check_is_admin)):
    log_usage(db, user.id, request)
    logs = db.query(db_model.UsageLog).order_by(db_model.UsageLog.id.desc()).offset(skip).limit(limit).all()
    if not logs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="No logs have been created yet.")
    return logs