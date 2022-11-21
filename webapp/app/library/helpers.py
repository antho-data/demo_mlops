from os import getenv, path
import markdown
from jose import jwt
import templates
import requests
from settings import config


def is_back_office():
    """is_back_office : return True if current web app is back-office instance
    :return: True or False
    """      
    return getenv("od_webapp_instance")=="BO"

def append_instance_shortname(dummy : str):
    """append_instance_shortname : jinja filter to append instance shortname
    :return: dummy arg (typically "") with suffix appended
    """  
    return dummy + getenv("od_webapp_instance")

def append_instance(title : str):
    """append_instance : jinja filter to append instance name from templates
    :return: title with suffix appended
    """       
    if getenv("od_webapp_instance")=="FO":
        return title + " -- Front Office"
    else : return title + " -- Back Office"
    
def get_api_url( )->str:
    """get_api_url : return API URL based on environment variable
    :return: root URL of the API
    """   
    api_root = getenv("api_root_url") +"/"
    return api_root

def md_to_html(filename : str):
    """md_to_html : transform markdown to HTML.
    :param filename: path to markdown file
    :return: HTML generated from makdown
    """
    filepath = path.join("app/pages/", filename)
    with open(filepath, "r", encoding="utf-8") as input_file:
        text = input_file.read()

    html = markdown.markdown(text)
    data = {
        "text": html
    }
    return data

def get_bare_token_from_cookie(request):
    """get_bare_token_from_cookie : extract the bare token from "acces_token" cookies (without "Bearer ")
    :param request: HTTP request coming in (with JWT token expected in cookie)
    :return: token (None if not found)
    """
    # Retrieve access token from cookie
    cookie_value = request.cookies.get("access_token")
    token = None
    if cookie_value:
        # Split cookie value to retrieve the token itself
        _, _, token  = cookie_value.partition(" ")

    return token

def check_authorization(request, requires_admin : bool = False):
    """check_authorization chek if user is authorized basd on JWT token.
    :param request: HTTP request coming in (with JWT token expected in cookie)
    :param requires_admin: true if admin privileges are required.   
    :return: token:str, authorized:bool, error:str
    """
    authorized = False
    error = None

    token = get_bare_token_from_cookie(request)
    if not token:
        return None, False, "You must first authenticate before using the selected option."

    # Verify that the acces token is valid
    try:
        
        # Retrieve security settings from configuration and try to decode JWT token
        sec_conf = config.get("security")  
        decoded_token = jwt.decode(token, sec_conf.get("secret"), sec_conf.get("algorithm"))
        if (requires_admin and decoded_token.get("role")!="administrator"):
            authorized=False
            error = "This operation requires administrator privileges.  Please log in as admin."
        else: 
            authorized = True
    except jwt.JWTError:
        error = "The signature of your access token is invalid (JWTError)."
    except jwt.ExpiredSignatureError:
        error = "Your session has expired, please login again (ExpiredSignatureError)."
    except jwt.JWTClaimsError:
        merrorsg = "There are invalid claims in your access token, please authenticate again (JWTClaimsError)."

    return token, authorized, error
    
