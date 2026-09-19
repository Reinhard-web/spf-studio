from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth.current_user import get_current_user
from app.db.models import Opportunity, Problem, User
from app.db.session import get_db
from app.schemas.opportunity import (
    OpportunityCreate,
    OpportunityResponse,
    OpportunityUpdate,
)
from app.tenants.context import CurrentOrganization

router = APIRouter(
    prefix="/innovation/opportunities",
    tags=["Innovation - Opportunities"],
)


@router.post(
    "",
    response_model=OpportunityResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_opportunity(
    data: OpportunityCreate,
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
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Problem not found in this organization",
            )

    opportunity = Opportunity(
        organization_id=organization.id,
        problem_id=data.problem_id,
        title=data.title,
        description=data.description,
        thesis=data.thesis,
        target_users=data.target_users,
        value_proposition=data.value_proposition,
        potential_outcome=data.potential_outcome,
        technology_leverage=data.technology_leverage,
        strategic_relevance=data.strategic_relevance,
        timing=data.timing,
        status=data.status,
    )

    db.add(opportunity)
    db.commit()
    db.refresh(opportunity)

    return opportunity


@router.get(
    "",
    response_model=list[OpportunityResponse],
)
def list_opportunities(
    organization: CurrentOrganization,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    result = db.execute(
        select(Opportunity)
        .where(Opportunity.organization_id == organization.id)
        .order_by(Opportunity.created_at.desc())
    )

    return result.scalars().all()


@router.get(
    "/{opportunity_id}",
    response_model=OpportunityResponse,
)
def get_opportunity(
    opportunity_id: int,
    organization: CurrentOrganization,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    opportunity = db.scalar(
        select(Opportunity).where(
            Opportunity.id == opportunity_id,
            Opportunity.organization_id == organization.id,
        )
    )

    if opportunity is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Opportunity not found",
        )

    return opportunity


@router.patch(
    "/{opportunity_id}",
    response_model=OpportunityResponse,
)
def update_opportunity(
    opportunity_id: int,
    data: OpportunityUpdate,
    organization: CurrentOrganization,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    opportunity = db.scalar(
        select(Opportunity).where(
            Opportunity.id == opportunity_id,
            Opportunity.organization_id == organization.id,
        )
    )

    if opportunity is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Opportunity not found",
        )

    updates = data.model_dump(exclude_unset=True)

    if "problem_id" in updates and updates["problem_id"] is not None:
        problem = db.scalar(
            select(Problem).where(
                Problem.id == updates["problem_id"],
                Problem.organization_id == organization.id,
            )
        )

        if problem is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Problem not found in this organization",
            )

    for field, value in updates.items():
        setattr(opportunity, field, value)

    db.commit()
    db.refresh(opportunity)

    return opportunity