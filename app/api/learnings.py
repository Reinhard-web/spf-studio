from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth.current_user import get_current_user
from app.db.models import Experiment, Learning, User
from app.db.session import get_db
from app.schemas.learning import LearningCreate, LearningResponse, LearningUpdate
from app.tenants.context import CurrentOrganization

router = APIRouter(
    prefix="/innovation/learnings",
    tags=["Innovation - Learnings"],
)


@router.post(
    "",
    response_model=LearningResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_learning(
    data: LearningCreate,
    organization: CurrentOrganization,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if data.experiment_id is not None:
        experiment = db.scalar(
            select(Experiment).where(
                Experiment.id == data.experiment_id,
                Experiment.organization_id == organization.id,
            )
        )

        if experiment is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Experiment not found in this organization",
            )

    learning = Learning(
        organization_id=organization.id,
        experiment_id=data.experiment_id,
        title=data.title,
        description=data.description,
        learning_type=data.learning_type,
        confidence=data.confidence,
        status=data.status,
    )

    db.add(learning)
    db.commit()
    db.refresh(learning)

    return learning


@router.get(
    "",
    response_model=list[LearningResponse],
)
def list_learnings(
    organization: CurrentOrganization,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    result = db.execute(
        select(Learning)
        .where(Learning.organization_id == organization.id)
        .order_by(Learning.created_at.desc())
    )

    return result.scalars().all()


@router.get(
    "/{learning_id}",
    response_model=LearningResponse,
)
def get_learning(
    learning_id: int,
    organization: CurrentOrganization,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    learning = db.scalar(
        select(Learning).where(
            Learning.id == learning_id,
            Learning.organization_id == organization.id,
        )
    )

    if learning is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Learning not found",
        )

    return learning


@router.patch(
    "/{learning_id}",
    response_model=LearningResponse,
)
def update_learning(
    learning_id: int,
    data: LearningUpdate,
    organization: CurrentOrganization,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    learning = db.scalar(
        select(Learning).where(
            Learning.id == learning_id,
            Learning.organization_id == organization.id,
        )
    )

    if learning is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Learning not found",
        )

    updates = data.model_dump(exclude_unset=True)

    for field, value in updates.items():
        setattr(learning, field, value)

    db.commit()
    db.refresh(learning)

    return learning