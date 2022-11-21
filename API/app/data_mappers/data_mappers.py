# coding: utf-8
from sqlalchemy import CHAR, Column, Date, DateTime, Float, ForeignKey, Index, String, Text, Time, VARBINARY, text, BIGINT, SMALLINT, VARCHAR, TEXT
from sqlalchemy.dialects.postgresql import SMALLINT, INTEGER, TEXT, BOOLEAN
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

UsersBase = declarative_base()
LogsBase =  declarative_base()

class User(UsersBase):
    __tablename__ = 'user'

    id = Column(INTEGER, autoincrement=True, primary_key = True)
    username = Column(String(50), nullable = False)
    password = Column(String(100), nullable = False)
    registered_on = Column(DateTime, nullable=True, server_default = text("CURRENT_TIMESTAMP"))
    is_admin = Column(BOOLEAN, nullable=False, server_default=text("'0'"))

class UsageLog(LogsBase):
    __tablename__ = 'usage_log'

    id = Column(INTEGER, autoincrement=True, primary_key = True)
    time_stamp = Column(DateTime, nullable=True, server_default = text("CURRENT_TIMESTAMP"))
    userid = Column(INTEGER)
    api_route = Column(String(255), nullable = False)

class OperationalLog(LogsBase):
    __tablename__ = 'operational_log'

    id = Column(INTEGER, autoincrement=True, primary_key = True)
    time_stamp = Column(DateTime, nullable=True, server_default = text("CURRENT_TIMESTAMP"))
    severity = Column(String(10), nullable = False)
    message = Column(String(255), nullable = False)
    context = Column(String(255), nullable = False)

