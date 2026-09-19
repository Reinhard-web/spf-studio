from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.auth.current_user import get_current_user
from app.db.models import (
    Decision,
    Evidence,
    Experiment,
    Idea,
    Learning,
    Opportunity,
    Problem,
    User,
)
from app.db.session import get_db
from app.schemas.innovation_dashboard import InnovationDashboardResponse
from app.tenants.context import CurrentOrganization

router = APIRouter(
    prefix="/innovation/dashboard",
    tags=["Innovation - Dashboard"],
)


@router.get(
    "",
    response_model=InnovationDashboardResponse,
)
def get_innovation_dashboard(
    organization: CurrentOrganization,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    def count_records(model):
        return db.scalar(
            select(func.count()).select_from(model).where(
                model.organization_id == organization.id
            )
        ) or 0

    problems_count = count_records(Problem)
    opportunities_count = count_records(Opportunity)
    ideas_count = count_records(Idea)
    experiments_count = count_records(Experiment)
    learnings_count = count_records(Learning)
    evidence_count = count_records(Evidence)
    decisions_count = count_records(Decision)

    experiments_running = db.scalar(
        select(func.count()).select_from(Experiment).where(
            Experiment.organization_id == organization.id,
            Experiment.status == "running",
        )
    ) or 0

    experiments_completed = db.scalar(
        select(func.count()).select_from(Experiment).where(
            Experiment.organization_id == organization.id,
            Experiment.status == "completed",
        )
    ) or 0

    unvalidated_experiments = db.scalar(
        select(func.count()).select_from(Experiment).where(
            Experiment.organization_id == organization.id,
            Experiment.outcome == "Inconclusive",
        )
    ) or 0

    if unvalidated_experiments > 0:
        current_focus = "Customer validation"
        next_actions = [
            "Conduct real-world customer interviews.",
            "Test prototypes with potential users.",
            "Capture customer evidence before making further product commitments.",
        ]
    elif experiments_running > 0:
        current_focus = "Experiment execution"
        next_actions = [
            "Complete the active experiments.",
            "Record results and outcomes.",
            "Capture learnings and supporting evidence.",
        ]
    elif problems_count == 0:
        current_focus = "Problem discovery"
        next_actions = [
            "Identify and document a meaningful problem.",
        ]
    else:
        current_focus = "Innovation pipeline"
        next_actions = [
            "Review the current innovation pipeline.",
            "Identify the next experiment to run.",
            "Capture evidence and learning as experiments progress.",
        ]

    return InnovationDashboardResponse(
        problems_count=problems_count,
        opportunities_count=opportunities_count,
        ideas_count=ideas_count,
        experiments_count=experiments_count,
        learnings_count=learnings_count,
        evidence_count=evidence_count,
        decisions_count=decisions_count,
        experiments_running=experiments_running,
        experiments_completed=experiments_completed,
        unvalidated_experiments=unvalidated_experiments,
        current_focus=current_focus,
        next_actions=next_actions,
    )