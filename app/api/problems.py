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
from app.schemas.problem import ProblemCreate, ProblemResponse, ProblemUpdate
from app.tenants.context import CurrentOrganization

router = APIRouter(
    prefix="/innovation/problems",
    tags=["Innovation - Problems"],
)


@router.post(
    "",
    response_model=ProblemResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_problem(
    data: ProblemCreate,
    organization: CurrentOrganization,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    problem = Problem(
        organization_id=organization.id,
        title=data.title,
        description=data.description,
        status=data.status,
        domain=data.domain,
        source_type=data.source_type,
        source_reference=data.source_reference,
        discovered_by=data.discovered_by,
        urgency=data.urgency,
        impact_potential=data.impact_potential,
        strategic_relevance=data.strategic_relevance,
    )

    db.add(problem)
    db.commit()
    db.refresh(problem)

    return problem


@router.get(
    "",
    response_model=list[ProblemResponse],
)
def list_problems(
    organization: CurrentOrganization,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    result = db.execute(
        select(Problem)
        .where(Problem.organization_id == organization.id)
        .order_by(Problem.created_at.desc())
    )

    return result.scalars().all()


@router.get(
    "/{problem_id}",
    response_model=ProblemResponse,
)
def get_problem(
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

    return problem


@router.patch(
    "/{problem_id}",
    response_model=ProblemResponse,
)
def update_problem(
    problem_id: int,
    data: ProblemUpdate,
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

    updates = data.model_dump(exclude_unset=True)

    for field, value in updates.items():
        setattr(problem, field, value)

    db.commit()
    db.refresh(problem)

    return problem

@router.get("/{problem_id}/journey")
def get_problem_journey(
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

    return {
        "problem": problem,
        "opportunity": opportunity,
        "idea": idea,
        "experiment": experiment,
        "learning": learning,
        "evidence": evidence,
        "decision": decision,
    }
   