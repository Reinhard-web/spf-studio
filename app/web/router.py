from pathlib import Path
from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter()

BASE_DIR = Path(__file__).resolve().parent


@router.get("/", include_in_schema=False)
def command_center_page():
    return FileResponse(BASE_DIR / "index.html")


@router.get("/login", include_in_schema=False)
def login_page():
    return FileResponse(BASE_DIR / "login.html")


@router.get("/smart-city", include_in_schema=False)
def smart_city_page():
    return FileResponse(BASE_DIR / "smart-city.html")


@router.get("/innovation", include_in_schema=False)
def innovation_page():
    return FileResponse(BASE_DIR / "innovation.html")


@router.get("/future-intelligence", include_in_schema=False)
def future_intelligence_page():
    return FileResponse(BASE_DIR / "future-intelligence.html")


@router.get("/labs", include_in_schema=False)
def labs_page():
    return FileResponse(BASE_DIR / "labs.html")


@router.get("/factory", include_in_schema=False)
def factory_page():
    return FileResponse(BASE_DIR / "factory.html")


@router.get("/studios", include_in_schema=False)
def studios_page():
    return FileResponse(BASE_DIR / "studios.html")


@router.get("/build-launch", include_in_schema=False)
def build_launch_page():
    return FileResponse(BASE_DIR / "build-launch.html")


@router.get("/operations", include_in_schema=False)
def operations_page():
    return FileResponse(BASE_DIR / "operations.html")


@router.get("/project-workspace", include_in_schema=False)
def projects_page():
    return FileResponse(BASE_DIR / "projects.html")


@router.get("/project-workspace/{project_id}", include_in_schema=False)
def project_workspace_page(project_id: int):
    return FileResponse(BASE_DIR / "project-workspace.html")


@router.get("/products", include_in_schema=False)
def products_page():
    return FileResponse(BASE_DIR / "products.html")


@router.get("/tasks", include_in_schema=False)
def tasks_page():
    return FileResponse(BASE_DIR / "tasks.html")


@router.get("/analytics", include_in_schema=False)
def analytics_page():
    return FileResponse(BASE_DIR / "analytics.html")


@router.get("/settings", include_in_schema=False)
def settings_page():
    return FileResponse(BASE_DIR / "settings.html")

@router.get("/ai-safety", include_in_schema=False)
def ai_safety_page():
    return FileResponse(BASE_DIR / "ai-safety.html")


@router.get("/autonomous-work", include_in_schema=False)
def autonomous_work_page():
    return FileResponse(BASE_DIR / "autonomous-work.html")


@router.get("/smart-agriculture", include_in_schema=False)
def smart_agriculture_page():
    return FileResponse(BASE_DIR / "smart-agriculture.html")


@router.get("/human-adaptation", include_in_schema=False)
def human_adaptation_page():
    return FileResponse(BASE_DIR / "human-adaptation.html")
