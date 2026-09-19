from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth.current_user import get_current_user
from app.db.models import Experiment, Idea, User
from app.db.session import get_db
from app.schemas.experiment import (
    ExperimentCreate,
    ExperimentResponse,
    ExperimentUpdate,
)
from app.tenants.context import CurrentOrganization

router = APIRouter(
    prefix="/innovation/experiments",
    tags=["Innovation - Experiments"],
)


@router.post(
    "",
    response_model=ExperimentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_experiment(
    data: ExperimentCreate,
    organization: CurrentOrganization,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    idea = db.scalar(
        select(Idea).where(
            Idea.id == data.idea_id,
            Idea.organization_id == organization.id,
        )
    )

    if idea is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Idea not found in this organization",
        )

    experiment = Experiment(
        organization_id=organization.id,
        idea_id=data.idea_id,
        title=data.title,
        objective=data.objective,
        hypothesis=data.hypothesis,
        uncertainty=data.uncertainty,
        assumptions=data.assumptions,
        methodology=data.methodology,
        success_criteria=data.success_criteria,
        failure_criteria=data.failure_criteria,
        status=data.status,
    )

    db.add(experiment)
    db.commit()
    db.refresh(experiment)

    return experiment


@router.get(
    "",
    response_model=list[ExperimentResponse],
)
def list_experiments(
    organization: CurrentOrganization,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    result = db.execute(
        select(Experiment)
        .where(Experiment.organization_id == organization.id)
        .order_by(Experiment.created_at.desc())
    )

    return result.scalars().all()


@router.get(
    "/{experiment_id}",
    response_model=ExperimentResponse,
)
def get_experiment(
    experiment_id: int,
    organization: CurrentOrganization,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    experiment = db.scalar(
        select(Experiment).where(
            Experiment.id == experiment_id,
            Experiment.organization_id == organization.id,
        )
    )

    if experiment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Experiment not found",
        )

    return experiment


@router.patch(
    "/{experiment_id}",
    response_model=ExperimentResponse,
)
def update_experiment(
    experiment_id: int,
    data: ExperimentUpdate,
    organization: CurrentOrganization,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    experiment = db.scalar(
        select(Experiment).where(
            Experiment.id == experiment_id,
            Experiment.organization_id == organization.id,
        )
    )

    if experiment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Experiment not found",
        )

    updates = data.model_dump(exclude_unset=True)

    for field, value in updates.items():
        setattr(experiment, field, value)

    db.commit()
    db.refresh(experiment)

    return experiment