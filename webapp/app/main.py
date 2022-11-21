from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.library.helpers import *
from app.routers import detection, login, usage_logs, operational_logs, reset_databases
from settings import config

print(append_instance("Start of Object Detection Web App"))

app = FastAPI()

# Add template instance to the app variable so that the custom filters added here below
# become available for each router.  app instance is accessible via request.app

app.templates = Jinja2Templates(directory="templates")

# Add custom filters to the templates so as to distinguish FO / BO from HTML templates

app.templates.env.filters["append_instance"]=append_instance
app.templates.env.filters["append_instance_shortname"]=append_instance_shortname

# Static content 

app.mount("/static", StaticFiles(directory="static"), name="static")

# Add our routers for dynamic content

app.include_router(login.router)
app.include_router(detection.router)
if is_back_office():
    app.include_router(usage_logs.router)
    app.include_router(operational_logs.router)
    app.include_router(reset_databases.router)

# Define route for root 

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    data = md_to_html("home.md")
    return app.templates.TemplateResponse("page.html", {"request": request, "data": data})

# Define routes to markdown pages in page subfolder

@app.get("/page/{page_name}", response_class=HTMLResponse)
async def show_page(request: Request, page_name: str):
    data = md_to_html(page_name+".md")
    return app.templates.TemplateResponse("page.html", {"request": request, "data": data})
