from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.auth import router as auth_router
from app.api.decisions import router as decisions_router
from app.api.evidence import router as evidence_router
from app.api.experiments import router as experiments_router
from app.api.ideas import router as ideas_router
from app.api.learnings import router as learnings_router
from app.api.memberships import router as memberships_router
from app.api.opportunities import router as opportunities_router
from app.api.opportunity_ideas import router as opportunity_ideas_router
from app.api.organizations import router as organizations_router
from app.api.problems import router as problems_router
from app.core.config import settings
from app.api.workflows import router as workflows_router
from app.api.workflow_summary import router as workflow_summary_router
from app.api.innovation_dashboard import router as innovation_dashboard_router
from app.web.router import router as web_router

app = FastAPI(title=settings.app_name)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8000", "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(organizations_router)
app.include_router(memberships_router)
app.include_router(problems_router)
app.include_router(opportunities_router)
app.include_router(ideas_router)
app.include_router(opportunity_ideas_router)
app.include_router(experiments_router)
app.include_router(learnings_router)
app.include_router(evidence_router)
app.include_router(decisions_router)
app.include_router(workflows_router)
app.include_router(workflow_summary_router)
app.include_router(innovation_dashboard_router)
app.include_router(web_router)