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
from app.schemas.workflow_summary import InnovationWorkflowSummaryResponse
from app.tenants.context import CurrentOrganization

router = APIRouter(
    prefix="/innovation/workflow-summary",
    tags=["Innovation - Workflow Summary"],
)


@router.get(
    "/{problem_id}",
    response_model=InnovationWorkflowSummaryResponse,
)
def get_workflow_summary(
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

    if decision is not None:
        current_stage = "decision"
    elif evidence is not None:
        current_stage = "evidence"
    elif learning is not None:
        current_stage = "learning"
    elif experiment is not None:
        current_stage = "experiment"
    elif idea is not None:
        current_stage = "idea"
    elif opportunity is not None:
        current_stage = "opportunity"
    else:
        current_stage = "problem"

    experiment_status = experiment.status if experiment else None
    experiment_outcome = experiment.outcome if experiment else None

    if experiment is None:
        validation_status = "not_tested"
        summary = (
            "The innovation chain has not yet reached an experiment, "
            "so there is no experiment-based validation."
        )
        next_action = "Define and run an experiment."
    elif experiment.outcome == "Inconclusive":
        validation_status = "unvalidated"
        summary = (
            "The experiment workflow was completed, but the available "
            "evidence does not establish real-world customer validation."
        )
        next_action = (
            "Conduct real-world customer interviews and prototype testing."
        )
    elif experiment.outcome:
        validation_status = "tested"
        summary = (
            f"The experiment completed with outcome: "
            f"{experiment.outcome}."
        )
        next_action = "Review the evidence and determine the next decision."
    else:
        validation_status = "in_progress"
        summary = (
            "An experiment exists, but its outcome has not yet been recorded."
        )
        next_action = "Complete the experiment and record its outcome."

    return InnovationWorkflowSummaryResponse(
        problem_id=problem.id,
        problem_title=problem.title,
        opportunity_id=opportunity.id if opportunity else None,
        idea_id=idea.id if idea else None,
        experiment_id=experiment.id if experiment else None,
        learning_id=learning.id if learning else None,
        evidence_id=evidence.id if evidence else None,
        decision_id=decision.id if decision else None,
        current_stage=current_stage,
        experiment_status=experiment_status,
        experiment_outcome=experiment_outcome,
        summary=summary,
        validation_status=validation_status,
        next_action=next_action,
    )