
from fastapi import Depends, FastAPI, HTTPException, status, APIRouter, Request
from fastapi.security import  OAuth2PasswordRequestForm
from pydantic import BaseModel
from app.database.database_init import get_user_session, get_log_session
from sqlalchemy.orm import Session
from app.library.helpers import *
from app.database.repository import authenticate_user
from app.library.logging import log_usage

# API instanciation

router = APIRouter(
    tags=["Login"],
    responses={401: {"description": "Not authenticated"}, 404: {"description": "Not found"}}
)


# Endpoint to test access token generation

class Token(BaseModel):
    access_token: str
    token_type: str

@router.post("/token", response_model=Token)
async def login_for_access_token(request : Request, 
                                form_data: OAuth2PasswordRequestForm = Depends(), 
                                db_user: Session = Depends(get_user_session),
                                db_log: Session = Depends(get_log_session)
                                ):
    user = authenticate_user(db = db_user, username = form_data.username, password = form_data.password)
    log_usage(db_log, user.id, request)          
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(user.username, user.is_admin)
    return {"access_token": access_token, "token_type": "bearer"}