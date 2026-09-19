from pydantic import BaseModel


class InnovationWorkflowSummaryResponse(BaseModel):
    problem_id: int
    problem_title: str

    opportunity_id: int | None
    idea_id: int | None
    experiment_id: int | None
    learning_id: int | None
    evidence_id: int | None
    decision_id: int | None

    current_stage: str
    experiment_status: str | None
    experiment_outcome: str | None

    summary: str
    validation_status: str
    next_action: str