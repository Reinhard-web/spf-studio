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
from app.schemas.decision import DecisionCreate, DecisionResponse, DecisionUpdate
from app.tenants.context import CurrentOrganization

router = APIRouter(
    prefix="/innovation/decisions",
    tags=["Innovation - Decisions"],
)


@router.post(
    "",
    response_model=DecisionResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_decision(
    data: DecisionCreate,
    organization: CurrentOrganization,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if data.problem_id is not None:
        problem = db.scalar(
            select(Problem).where(
                Problem.id == data.problem_id,
                Problem.organization_id == organization.id,
            )
        )
        if problem is None:
            raise HTTPException(status_code=404, detail="Problem not found")

    if data.opportunity_id is not None:
        opportunity = db.scalar(
            select(Opportunity).where(
                Opportunity.id == data.opportunity_id,
                Opportunity.organization_id == organization.id,
            )
        )
        if opportunity is None:
            raise HTTPException(status_code=404, detail="Opportunity not found")

    if data.idea_id is not None:
        idea = db.scalar(
            select(Idea).where(
                Idea.id == data.idea_id,
                Idea.organization_id == organization.id,
            )
        )
        if idea is None:
            raise HTTPException(status_code=404, detail="Idea not found")

    if data.experiment_id is not None:
        experiment = db.scalar(
            select(Experiment).where(
                Experiment.id == data.experiment_id,
                Experiment.organization_id == organization.id,
            )
        )
        if experiment is None:
            raise HTTPException(status_code=404, detail="Experiment not found")

    if data.learning_id is not None:
        learning = db.scalar(
            select(Learning).where(
                Learning.id == data.learning_id,
                Learning.organization_id == organization.id,
            )
        )
        if learning is None:
            raise HTTPException(status_code=404, detail="Learning not found")

    if data.evidence_id is not None:
        evidence = db.scalar(
            select(Evidence).where(
                Evidence.id == data.evidence_id,
                Evidence.organization_id == organization.id,
            )
        )
        if evidence is None:
            raise HTTPException(status_code=404, detail="Evidence not found")

    decision = Decision(
        organization_id=organization.id,
        problem_id=data.problem_id,
        opportunity_id=data.opportunity_id,
        idea_id=data.idea_id,
        experiment_id=data.experiment_id,
        learning_id=data.learning_id,
        evidence_id=data.evidence_id,
        title=data.title,
        decision=data.decision,
        rationale=data.rationale,
        status=data.status,
        decided_by=data.decided_by,
    )

    db.add(decision)
    db.commit()
    db.refresh(decision)

    return decision


@router.get(
    "",
    response_model=list[DecisionResponse],
)
def list_decisions(
    organization: CurrentOrganization,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return db.scalars(
        select(Decision)
        .where(Decision.organization_id == organization.id)
        .order_by(Decision.id)
    ).all()


@router.get(
    "/{decision_id}",
    response_model=DecisionResponse,
)
def get_decision(
    decision_id: int,
    organization: CurrentOrganization,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    decision = db.scalar(
        select(Decision).where(
            Decision.id == decision_id,
            Decision.organization_id == organization.id,
        )
    )

    if decision is None:
        raise HTTPException(status_code=404, detail="Decision not found")

    return decision


@router.patch(
    "/{decision_id}",
    response_model=DecisionResponse,
)
def update_decision(
    decision_id: int,
    data: DecisionUpdate,
    organization: CurrentOrganization,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    decision = db.scalar(
        select(Decision).where(
            Decision.id == decision_id,
            Decision.organization_id == organization.id,
        )
    )

    if decision is None:
        raise HTTPException(status_code=404, detail="Decision not found")

    updates = data.model_dump(exclude_unset=True)

    for field, value in updates.items():
        setattr(decision, field, value)

    db.commit()
    db.refresh(decision)

    return decision