from fastapi import Request, APIRouter, Form, UploadFile, File
from fastapi.responses import HTMLResponse, FileResponse, Response
from fastapi.templating import Jinja2Templates
import requests
from settings import config
from urllib3 import encode_multipart_formdata
from os import getenv
from app.library.helpers import *

router = APIRouter()


@router.get("/detection", response_class=HTMLResponse)
async def detection(request: Request):
    token, auth, error = check_authorization(request)
    if auth==False:
        return request.app.templates.TemplateResponse("login.html", {"request": request,  "error": error})
    return request.app.templates.TemplateResponse("detection.html", {"request": request})

@router.post("/detection", response_class=FileResponse)
async def detection(request: Request, file: UploadFile = File(...)):
    # Check authorization 

    token, auth, error = check_authorization(request)
    if auth==False:
        return request.app.templates.TemplateResponse("login.html", {"request": request,  "error": error})

    # Read file content 
    file_content = await file.read()

    # Build the multipart body
    fields = {  "file": (file.filename, file_content, "application/octet-stream"), }  # or "image/jpeg"
    body, content_type = encode_multipart_formdata(fields)

    # Post the request to the prediction route of the API 

    resp = requests.post(   
                            get_api_url() + "detection", 
                            data = body,
                            headers={ "accept": "application/json",
                                    "Authorization": "Bearer " + token,
                                    "Content-Type" : content_type }, 
                         )
                 
    if resp.status_code!=200:
        return  request.app.templates.TemplateResponse("detection.html", {"request": request, "error" : "Bad request" + resp.status_code})

    return Response(content=resp.content, media_type="image/png")