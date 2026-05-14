import uuid
from typing import List
from pydantic import BaseModel, Field
from src.agents.thinker.state import IdeaNode


class GlobalState(BaseModel):
    problem_statement: str
    current_code: str = ""
    current_best_score: float = 0.0
    
    # context - e.g what has been tried and didn't work since the last successful iteration
    history: List[str] = []

    # Thinker ideas, the first being the best one
    candidate_ideas: List[IdeaNode] = []
