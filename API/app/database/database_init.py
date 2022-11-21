from warnings import catch_warnings
from sqlalchemy import create_engine, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.data_mappers.data_mappers import UsersBase, LogsBase
from app.settings import config
from app.database.repository import *
from app.library.helpers import is_back_office
from app.library.logging import *

def get_db_url(config_section:str, config_sub_section:str)->str:
    conf =  config.get("database").get(config_section).get(config_sub_section)
    url = f"postgresql+psycopg2://{conf.get('POSTGRES_USER')}:{conf.get('POSTGRES_PASSWORD')}@{conf.get('POSTGRES_HOST')}:{conf.get('POSTGRES_PORT')}/{conf.get('POSTGRES_DB')}"
    print(f"Database url : {url}")
    return url

user_engine : None
logs_engine : None

def init_databases(environment : str, recreate_tables : bool):
    global user_engine 
    global logs_engine  
    user_engine = create_engine(get_db_url(environment, "users"))
    logs_engine = create_engine(get_db_url(environment, "logs")) 
    
    if recreate_tables:
        reset_databases()
    else:
        ensure_tables_exist()  

    if is_back_office():  
        db = next(get_user_session())
        user = get_user_admin(db = db, username = 'admin')
        if not user:
            create_default_users(db)


def ensure_tables_exist():
    if not is_back_office():
        return

    user_engine = get_engine("users")
    logs_engine = get_engine("logs")

    # If user table does not exist, we are in the very first start of Docker 
    # ==> create tables and default content 
    if not inspect(user_engine).has_table("user") :
        create_tables_and_default_users(user_engine, logs_engine)   

def reset_databases():
    if not is_back_office():
        return

    user_engine = get_engine("users")
    logs_engine = get_engine("logs")

    UsersBase.metadata.drop_all(bind=user_engine)
    LogsBase.metadata.drop_all(bind=logs_engine)

    create_tables_and_default_users(user_engine, logs_engine)

def create_tables_and_default_users(user_engine, log_engine):
    if not is_back_office():
        return

    UsersBase.metadata.create_all(bind=user_engine)
    LogsBase.metadata.create_all(bind=logs_engine)
    create_default_users(next(get_user_session()))
    create_operational_log(next(get_log_session()),  Severity.info.value, "Tables (re)created with default users.", instance_shortname())

def get_engine(db:str):
    if db=="users":
        return user_engine
    if db=="logs":
        return logs_engine

# Methods for dependency injection

def get_user_session():
    sm = sessionmaker()
    sm.configure(binds={UsersBase:user_engine})
    session = sm()
    try:
        yield session
    finally:
        session.close()


def get_log_session():
    sm = sessionmaker()
    sm.configure(binds={LogsBase:logs_engine})
    session = sm()    
    try:
        yield session
    finally:
        session.close()   


