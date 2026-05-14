from src.agents.thinker.state import ThinkerState
from src.shared.client import THINKER_CLIENT as llm
from src.agents.main.state import IdeaNode

from langchain_core.prompts import ChatPromptTemplate
from typing import List
from pydantic import BaseModel

class BrainstormerOutput(BaseModel):
    ideas: List[IdeaNode]

def brainstormer(state: ThinkerState):
    """
    Proposes new ideas based on the problem statement, current code, and past failures (history).
    """
    history = "\n".join([f"- {h}" for h in state.history])
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", f"Propose 2-3 new ideas. AVOID these past failures:\n{history}"),
        ("user", f"Goal: {state.problem_statement}\nCurrent Code: {state.current_code}")
    ])

    chain = prompt | llm.with_structured_output(BrainstormerOutput)
    response = chain.invoke({})
    
    # Add new ideas to the global pool for the UI/Comparator to see
    return {"candidate_ideas": state.candidate_ideas + response.ideas}
