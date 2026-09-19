from pydantic import BaseModel


class OpportunityIdeaCreate(BaseModel):
    opportunity_id: int
    idea_id: int