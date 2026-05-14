from typing import List
from pydantic import BaseModel, Field

class IdeaNode(BaseModel):
    idea_id: str = Field(default_factory=lambda: uuid.uuid4().hex)
    title: str
    concept: str
    details: str
    p_success: float       # Probability of working
    p_local_minima: float  # Probability of a dead-end



class ThinkerState(BaseModel):
    problem_statement: str
    current_code: str = ""

    # same history as in the main state (remains unchanged as its managed by the main agent)
    history: List[str] = [] 

    candidate_ideas: List[IdeaNode] = []
