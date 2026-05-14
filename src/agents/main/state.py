import uuid
from typing import List
from pydantic import BaseModel, Field

class IdeaNode(BaseModel):
    idea_id: str = Field(default_factory=lambda: uuid.uuid4().hex)
    title: str
    concept: str
    details: str
    p_success: float       # Probability of working
    p_local_minima: float  # Probability of a dead-end

class GlobalState(BaseModel):
    problem_statement: str
    current_code: str = ""
    current_best_score: float = 0.0
    
    # context - e.g what has been tried and didn't work since the last successful iteration
    history: List[str] = []

    # Thinker ideas, the first being the best one
    candidate_ideas: List[IdeaNode] = []
