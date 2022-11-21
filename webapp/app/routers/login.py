from fastapi import FastAPI, Request, Form, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordRequestForm
import requests
import json
from settings import config
from app.library.helpers import *

router = APIRouter()

@router.get("/login", response_class=HTMLResponse)
def login_get(request: Request):
    return request.app.templates.TemplateResponse('login.html', context={'request': request})

@router.post("/login")
async def login_post(request: Request):
    form = await request.form()
    username = form.get("username")
    password = form.get("password")

    # The following code is normally not need since both the fiels are mandatory
    # but it is easy to remove the "required" attribute client-side with Chrome developper tools.
    # Better be safe than sorry !

    errors = []
    if not username:
        errors.append("Please enter a valid usename")
    if not password:
        errors.append("Password enter your password")
    if len(errors) > 0:
        return request.app.templates.TemplateResponse("login.html", {"request": request, "error":' -- '.join(errors)}) 

    # Post to the API a request for token  with the credentials provided by the user

    resp = requests.post(get_api_url()+"token", 
                        data={"username": username, "password": password, "grant_type": "password"},
                        headers={"content-type": "application/x-www-form-urlencoded"})
    
    # Check the response of the API 
    
    if (resp.status_code==200):
        data = json.loads(resp.text)
        response = request.app.templates.TemplateResponse("login.html", {"request": request, "message": "Login succesful."})
        response.set_cookie(key="access_token", value=f"Bearer {data['access_token']}", httponly=True)
    else:
        return request.app.templates.TemplateResponse("login.html", {"request": request, "error": "Invalid credentials !"}) 
    return response

