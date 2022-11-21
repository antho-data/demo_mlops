from fastapi import Request, APIRouter
from fastapi.responses import HTMLResponse
import requests
import json
from app.library.helpers import *

router = APIRouter()

@router.get("/operational_logs", response_class=HTMLResponse)
def login_get(request: Request, skip: int =0, limit: int=50):
    # Check authorization 

    token, auth, error = check_authorization(request, True)
    if auth==False:
        return request.app.templates.TemplateResponse("login.html", {"request": request,  "error": error})

    # Request operational logs records from API :

    resp = requests.get(get_api_url() + f"operational_logs?skip={skip}&limit={limit}", 
                        headers={ "accept": "application/json", "Authorization": "Bearer " + token }  )

    # Inject them in the HTML template :
                        
    return request.app.templates.TemplateResponse('operational_logs.html', 
                                context={'request': request, "logs" : json.loads(resp.content.decode('utf-8'))})

