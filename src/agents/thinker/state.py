from typing import List
from pydantic import BaseModel
from src.agents.main.state import IdeaNode

class ThinkerState(BaseModel):
    problem_statement: str
    current_code: str = ""

    # same history as in the main state (remains unchanged as its managed by the main agent)
    history: List[str] = [] 

    candidate_ideas: List[IdeaNode] = []
