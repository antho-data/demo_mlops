from fastapi import Depends, APIRouter, Request
from app.library.security import check_is_admin
from app.settings import config
from app.database.database_init import get_log_session, get_user_session, get_user_count
from sqlalchemy.orm import Session
from app.database.database_init import reset_databases, init_databases
from app.library.security import check_is_admin
from app.data_mappers.data_mappers import User
from app.library.logging import log_usage

# API instanciation
router = APIRouter(
    tags=["Maintenance"],
    responses={401: {"description": "Not authorized"}}    
)

@router.get('/reset_databases', description="Reset database to initial stated")
async def get_reset_database(   request : Request, 
                                db: Session = Depends(get_log_session), 
                                user: User = Depends(check_is_admin)):
    log_usage(db, user.id, request)  
    try:
        db.commit()
        db.close_all()
        init_databases("production", True)  
    except Exception as ex:
        print(ex)
      
    return str(get_user_count(next(get_user_session())))

