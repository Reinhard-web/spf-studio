from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
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
from app.schemas.workflow import InnovationWorkflowResponse
from app.tenants.context import CurrentOrganization

router = APIRouter(
    prefix="/innovation/workflows",
    tags=["Innovation - Workflows"],
)


def model_to_dict(model):
    return {
        column.name: getattr(model, column.name)
        for column in model.__table__.columns
    }


@router.get(
    "/{problem_id}",
    response_model=InnovationWorkflowResponse,
)
def get_innovation_workflow(
    problem_id: int,
    organization: CurrentOrganization,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    problem = db.scalar(
        select(Problem).where(
            Problem.id == problem_id,
            Problem.organization_id == organization.id,
        )
    )

    if problem is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Problem not found",
        )

    opportunity = db.scalar(
        select(Opportunity).where(
            Opportunity.problem_id == problem.id,
            Opportunity.organization_id == organization.id,
        )
    )

    idea = None
    if opportunity is not None:
        idea = db.scalar(
            select(Idea).where(
                Idea.opportunity_id == opportunity.id,
                Idea.organization_id == organization.id,
            )
        )

    experiment = None
    if idea is not None:
        experiment = db.scalar(
            select(Experiment).where(
                Experiment.idea_id == idea.id,
                Experiment.organization_id == organization.id,
            )
        )

    learning = None
    evidence = None

    if experiment is not None:
        learning = db.scalar(
            select(Learning).where(
                Learning.experiment_id == experiment.id,
                Learning.organization_id == organization.id,
            )
        )

        evidence = db.scalar(
            select(Evidence).where(
                Evidence.experiment_id == experiment.id,
                Evidence.organization_id == organization.id,
            )
        )

    decision = db.scalar(
        select(Decision).where(
            Decision.problem_id == problem.id,
            Decision.organization_id == organization.id,
        )
    )

    return InnovationWorkflowResponse(
        problem=model_to_dict(problem),
        opportunity=model_to_dict(opportunity) if opportunity else None,
        idea=model_to_dict(idea) if idea else None,
        experiment=model_to_dict(experiment) if experiment else None,
        learning=model_to_dict(learning) if learning else None,
        evidence=model_to_dict(evidence) if evidence else None,
        decision=model_to_dict(decision) if decision else None,
    )