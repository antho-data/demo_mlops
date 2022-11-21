from datetime import datetime
from app.data_mappers.data_mappers import UsersBase, LogsBase, User, UsageLog, OperationalLog
from sqlalchemy.orm import Session
from app.settings import config
from app.library.helpers import *
from fastapi import Depends, HTTPException, status
from sqlalchemy import func

# Query methods

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def get_user_admin(db: Session, username: str):
    return db.query(User).filter(User.is_admin==True).first()

def get_all_users(db: Session):
    return db.query(User).all()

def get_user_count(db: Session):
    return db.query(func.count(User.id)).scalar()

# Create methods

def create_default_admin(db:Session):
    db.add(User(username="admin", password= get_password_hash("admin"), is_admin= True ))
    db.commit()

def create_operational_log(db : Session, severity: str, message: str, context):
    log = OperationalLog()
    log.time_stamp = datetime.now()
    log.severity = severity
    log.message = message
    log.context = context
    db.add(log)
    db.commit()

def create_usage_log(db : Session, userid: str, route: str):
    log = UsageLog()
    log.userid=userid
    log.time_stamp = datetime.now()
    log.api_route = route
    db.add(log)
    db.commit()    

# Methods for authentication and authorization

def authenticate_user(db : Session, username: str, password: str):
    user = get_user_by_username(db = db, username = username)
    if not user:
        raise HTTPException(status_code = 401, detail = f"Username {username} not found !")    
    if not verify_password(password, user.password):
        raise HTTPException(status_code = 401, detail = f"Wrong password provide !")
    return user


# Methods for database initialization

def create_default_users(db : Session):
    db.add(User(username="admin", password= get_password_hash("admin"), is_admin= True ))
    db.add(User(username="noel", password= get_password_hash("noel"), is_admin= False ))
    db.add(User(username="francois", password= get_password_hash("francois"), is_admin= False ))
    db.commit()




