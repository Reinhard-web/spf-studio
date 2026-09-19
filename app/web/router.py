from pathlib import Path

from fastapi import APIRouter
from fastapi.responses import FileResponse


router = APIRouter()

BASE_DIR = Path(__file__).resolve().parent


@router.get("/", include_in_schema=False)
def command_center_page():
    return FileResponse(BASE_DIR / "index.html")


@router.get("/innovation", include_in_schema=False)
def innovation_page():
    return FileResponse(BASE_DIR / "innovation.html")