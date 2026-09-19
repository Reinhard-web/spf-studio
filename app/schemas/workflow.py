from pydantic import BaseModel


class InnovationWorkflowResponse(BaseModel):
    problem: dict
    opportunity: dict | None
    idea: dict | None
    experiment: dict | None
    learning: dict | None
    evidence: dict | None
    decision: dict | None