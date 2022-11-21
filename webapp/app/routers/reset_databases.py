from fastapi import Request, APIRouter, Form, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse, FileResponse, Response
from fastapi.templating import Jinja2Templates
import requests
from settings import config
from urllib3 import encode_multipart_formdata
from os import getenv
from app.library.helpers import *

router = APIRouter()


@router.get("/reset_databases", response_class=HTMLResponse)
async def get_reset_database(request: Request):
    # Check authorization 

    token, auth, error = check_authorization(request, True)
    if auth==False:
        return request.app.templates.TemplateResponse("login.html", {"request": request,  "error": error})

    return request.app.templates.TemplateResponse("reset_databases.html", {"request": request})


@router.post("/reset_databases", response_class=HTMLResponse)
async def post_reset_database(request: Request):

    # Check authorization 

    token, auth, error = check_authorization(request, True)
    if auth==False:
        return request.app.templates.TemplateResponse("login.html", {"request": request,  "error": error})

     # Post the request to the corresponding route of the API 

    resp = requests.get(   
                            get_api_url() + "reset_databases", 
                            headers={ "accept": "application/json", "Authorization": "Bearer " + token }
                    )
                
    if resp.status_code!=200:
        return  request.app.templates.TemplateResponse("reset_databases.html", {"request": request, "error" : f"Bad request : {resp.status_code}"})
    else: return  request.app.templates.TemplateResponse("reset_databases.html", {"request": request, "message" : "Database reset completed successfully !" })


