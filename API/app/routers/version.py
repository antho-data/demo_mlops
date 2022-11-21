from fastapi import Depends, APIRouter
from app.library.security import check_authenticated
from app.settings import config

# API instanciation
router = APIRouter(
    tags=["API state"],
    responses = {404: {"description": "Not found"}},
)

@router.get('/version', description="Return API version")
async def get_version():
    return config.get("api_version")