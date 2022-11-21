from os import getenv
from app.settings import config
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt


def instance_shortname():
    """instance_shortname : return "FO" or "BO" depending on runnings instance
    :return: "FO" / "BO"
    """      
    return "BO" if is_back_office() else "FO"

def is_back_office():
    """is_back_office : return True if current API is back-office instance
    :return: True or False
    """      
    return getenv("od_api_instance")=="BO"


def append_instance(title : str):
    """append_instance : append instance name to title
    :param title: application title to be decorated
    :return: titel + "-- Front/Back Office"
    """    
    if getenv("od_api_instance")=="FO":
        return title + " -- Front Office"
    else : return title + " -- Back Office"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Load security parameters

sec_conf = config.get("security")
SECRET_KEY = sec_conf.get("secret") # to get a string like this run: openssl rand -hex 32
ALGORITHM = sec_conf.get("algorithm")
ACCESS_TOKEN_EXPIRE_MINUTES = sec_conf.get("acces_token_expire_minutes")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(username: str, is_admin:bool):
    dic = { "sub": username, 
            "role" : "administrator" if is_admin else "user",
            "exp" : datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES) }
    encoded_jwt = jwt.encode(dic, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt    


