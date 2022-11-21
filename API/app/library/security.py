
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from app.database.database_init import get_user_session, get_log_session
from sqlalchemy.orm import Session
from app.library.helpers import *
from app.database.repository import get_user_by_username
from app.data_mappers.data_mappers import User


# Methods for authentication and autorization via dependency injection

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

authorization_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="You are not allowed to perform this operation.",
    headers={"WWW-Authenticate": "Bearer"},
)

async def check_authenticated(token: str = Depends(oauth2_scheme), db: Session = Depends(get_user_session)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise authorization_exception
    except JWTError:
        raise authorization_exception
    user = get_user_by_username(db = db, username=username)
    if user is None:
        raise authorization_exception
    return user


async def check_is_admin(token: str = Depends(oauth2_scheme), db: Session = Depends(get_user_session)):
    user = await check_authenticated(token, db)
    if not user.is_admin:
       raise authorization_exception
    return user