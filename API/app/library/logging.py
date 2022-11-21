from fastapi import Depends,  Header, Request
from sqlalchemy.orm import Session
from app.database.repository import create_usage_log, create_operational_log
from app.library.helpers import instance_shortname
from enum import Enum

class Severity(Enum):
    info =  'info'
    warning = 'warning'
    error = 'error'

# Methods for logging to usage logs and operational logs

def log_usage(db : Session, userid : int, request : Request):
    create_usage_log(db, userid,  request.method + " " + request.url.__str__())


def log_event(db : Session, severity: Severity, message: str, context: str=""):
    create_operational_log(db, severity.value, message, instance_shortname() + " " + context)

