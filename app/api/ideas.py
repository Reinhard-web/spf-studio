from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth.current_user import get_current_user
from app.db.models import Idea, Opportunity, User
from app.db.session import get_db
from app.schemas.idea import IdeaCreate, IdeaResponse, IdeaUpdate
from app.tenants.context import CurrentOrganization

router = APIRouter(
    prefix="/innovation/ideas",
    tags=["Innovation - Ideas"],
)


@router.post(
    "",
    response_model=IdeaResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_idea(
    data: IdeaCreate,
    organization: CurrentOrganization,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if data.opportunity_id is not None:
        opportunity = db.scalar(
            select(Opportunity).where(
                Opportunity.id == data.opportunity_id,
                Opportunity.organization_id == organization.id,
            )
        )

        if opportunity is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Opportunity not found",
            )

    idea = Idea(
        organization_id=organization.id,
        opportunity_id=data.opportunity_id,
        title=data.title,
        description=data.description,
        solution_concept=data.solution_concept,
        target_users=data.target_users,
        value_proposition=data.value_proposition,
        hypothesis=data.hypothesis,
        expected_outcome=data.expected_outcome,
        success_conditions=data.success_conditions,
        status=data.status,
    )

    db.add(idea)
    db.commit()
    db.refresh(idea)

    return idea


@router.get(
    "",
    response_model=list[IdeaResponse],
)
def list_ideas(
    organization: CurrentOrganization,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    result = db.execute(
        select(Idea)
        .where(Idea.organization_id == organization.id)
        .order_by(Idea.created_at.desc())
    )

    return result.scalars().all()


@router.get(
    "/{idea_id}",
    response_model=IdeaResponse,
)
def get_idea(
    idea_id: int,
    organization: CurrentOrganization,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    idea = db.scalar(
        select(Idea).where(
            Idea.id == idea_id,
            Idea.organization_id == organization.id,
        )
    )

    if idea is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Idea not found",
        )

    return idea


@router.patch(
    "/{idea_id}",
    response_model=IdeaResponse,
)
def update_idea(
    idea_id: int,
    data: IdeaUpdate,
    organization: CurrentOrganization,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    idea = db.scalar(
        select(Idea).where(
            Idea.id == idea_id,
            Idea.organization_id == organization.id,
        )
    )

    if idea is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Idea not found",
        )

    updates = data.model_dump(exclude_unset=True)

    if "opportunity_id" in updates and updates["opportunity_id"] is not None:
        opportunity = db.scalar(
            select(Opportunity).where(
                Opportunity.id == updates["opportunity_id"],
                Opportunity.organization_id == organization.id,
            )
        )

        if opportunity is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Opportunity not found",
            )

    for field, value in updates.items():
        setattr(idea, field, value)

    db.commit()
    db.refresh(idea)

    return idea