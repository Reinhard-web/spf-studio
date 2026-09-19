from pydantic import BaseModel


class InnovationDashboardResponse(BaseModel):
    problems_count: int
    opportunities_count: int
    ideas_count: int
    experiments_count: int
    learnings_count: int
    evidence_count: int
    decisions_count: int

    experiments_running: int
    experiments_completed: int
    unvalidated_experiments: int

    current_focus: str
    next_actions: list[str]