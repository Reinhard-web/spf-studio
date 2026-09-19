from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, text
from sqlalchemy.orm import Session

from app.auth.current_user import get_current_user
from app.db.models import Idea, Opportunity, User
from app.db.session import get_db
from app.schemas.opportunity_idea import OpportunityIdeaCreate
from app.tenants.context import CurrentOrganization

router = APIRouter(
    prefix="/innovation/opportunity-ideas",
    tags=["Innovation - Opportunity Ideas"],
)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
)
def link_opportunity_to_idea(
    data: OpportunityIdeaCreate,
    organization: CurrentOrganization,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    opportunity = db.scalar(
        select(Opportunity).where(
            Opportunity.id == data.opportunity_id,
            Opportunity.organization_id == organization.id,
        )
    )

    if opportunity is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Opportunity not found in this organization",
        )

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

    existing = db.execute(
        text(
            """
            SELECT 1
            FROM opportunity_ideas
            WHERE opportunity_id = :opportunity_id
              AND idea_id = :idea_id
            """
        ),
        {
            "opportunity_id": data.opportunity_id,
            "idea_id": data.idea_id,
        },
    ).first()

    if existing is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Opportunity is already linked to this idea",
        )

    db.execute(
        text(
            """
            INSERT INTO opportunity_ideas (opportunity_id, idea_id)
            VALUES (:opportunity_id, :idea_id)
            """
        ),
        {
            "opportunity_id": data.opportunity_id,
            "idea_id": data.idea_id,
        },
    )

    db.commit()

    return {
        "opportunity_id": data.opportunity_id,
        "idea_id": data.idea_id,
        "message": "Opportunity linked to idea successfully",
    }