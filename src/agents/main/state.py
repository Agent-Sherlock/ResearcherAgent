import uuid
from typing import List
from pydantic import BaseModel, Field
from src.agents.thinker.state import IdeaNode


class GlobalState(BaseModel):
    problem_statement: str = ""
    git_repo_name: str = ""
    current_code: str = ""
    current_best_score: float = 0.0
    
    # context - e.g what has been tried and didn't work since the last successful iteration
    history: List[str] = []

    # Thinker ideas, the first being the best one
    candidate_ideas: List[IdeaNode] = []

    # the output of the arena, describing the scope for improvement (so that the evaluation wont fail)
    improvement_scope: str = ""