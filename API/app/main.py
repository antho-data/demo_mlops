from app.data_mappers import data_mappers as model_sqlalchemy
from app.database.database_init import init_databases, get_engine, get_log_session
from os import getenv, path
from fastapi import FastAPI
from fastapi.responses import JSONResponse, FileResponse
from fastapi import Request, status as statuscode # avoid name conflict with status router
from fastapi.staticfiles import StaticFiles

from app.routers import status, status, version, detection, usage_logs, operational_logs, reset_databases, login
from app.yolo_interface.predictor import Predictor
from app.settings import config
from app.library.helpers import append_instance, is_back_office
from app.library.logging import log_event, Severity
import time
from sys import argv

print(append_instance("Start of Object Detection API"))

# Description header

description = """
Object detection API based on YOLOv7 model 

## API state (non-authenticated user)
Consult home page, API status and version 
* **Api home page**
* **Read API version**
* **Read API status**

## Object detection (authenticated user)
Perform object detection
* **Perform object detection on user-provided image**

## Logs (admin user)
Consult logs
* **Consult usage logs**
* **Consult operational logs**

## Maintenance (admin user)
System maintenance operations
* **Reset database to initial state**


## Login
Utility to test authentication process separately
* **Post access token**

"""

# Add description endpoint

tags_metadata = [
    {
        "name": "API state",
        "description": "Get API status, version, home page"
    },
    {
        "name": "Object detection",
        "description": "Perform object detection on user-provided image"
    },
    {
        "name": "Logs",
        "description": "Consult usage logs and operational logs"
    },
    {
        "name": "Maintenance",
        "description": "Reset database to initial state"
    } ,
    {
        "name": "Login",
        "description": "Authenticate username and password then create access token"
    },
]

app = FastAPI(
    title= append_instance("YOLOv7-based Object Detection API") ,
    description=description,
    openapi_tags=tags_metadata, 
    version=config.get("api_version")
)

# Init databases if not running from pyttest

if 'pytest' not in argv[0]:
    init_databases("production", False)

log_event(next(get_log_session()), Severity.info, append_instance("Start of Object Detection API"))

# Mount folder for static files

app.mount("/static", StaticFiles(directory="static"), name="static")

#region Startup and Exception handlers  

@app.on_event("startup")
async def startup_event():
    """" startup_event : setup Predictor class on startup """
    Predictor.init('model_params','input', 'output')

@app.exception_handler(ValueError) 
async def value_error_handler(request: Request, exc: ValueError):
    """ generic_exception_handler : captures and logs ValueError exceptions and returns HTTP 422 status code + detail """

    log_event(next(get_log_session()), Severity.error, exc.__str__())   
    return JSONResponse(status_code=statuscode.HTTP_422_UNPROCESSABLE_ENTITY, content = f"Invalid request :  {exc}" )

@app.exception_handler(Exception) 
async def generic_exception_handler(request: Request, exc: Exception):
    """ generic_exception_handler : captyres and logs any uncaught exception and returns HTTP 500 with exception detail """

    log_event(next(get_log_session()), Severity.error, exc.__str__())   
    return JSONResponse(status_code=statuscode.HTTP_500_INTERNAL_SERVER_ERROR, content = f"Uncaught exception :  {exc}" )
#endregion

#region Home route + favicon.ico 

@app.get('/', tags = ["API state"])
async def get_home_page():
    return {'data': append_instance('Hello from API')}

# The following is just to make the browser happy. 

@app.get('/favicon.ico', include_in_schema=False) #  Excluded from Swagger doc !
async def favicon():
    file_name = "favicon.ico"
    file_path = path.join(app.root_path, "static", file_name)
    return FileResponse(path=file_path, headers={"Content-Disposition": "attachment; filename=" + file_name})

#endregion

#region The routers implementing the actual API

app.include_router(version.router)
app.include_router(status.router)
app.include_router(detection.router)
app.include_router(login.router)
if (is_back_office()):
    app.include_router(usage_logs.router)
    app.include_router(operational_logs.router)
    app.include_router(reset_databases.router)

#endregion