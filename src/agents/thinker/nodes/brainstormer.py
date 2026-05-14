from src.agents.thinker.state import ThinkerState
from src.shared.client import THINKER_CLIENT as llm
from src.agents.thinker.state import IdeaNode
from src.agents.thinker.prompts import BRAINSTORM_SYSTEM_PROMPT
from src.shared.utils.general_utils import clean_docstring
from src.config.config import MIN_NEW_IDEA_COUNT, MAX_NEW_IDEA_COUNT

from typing import List
from pydantic import BaseModel, Field
from langchain_core.messages import SystemMessage, HumanMessage

class _BrainstormerOutput(BaseModel):
    ideas: List[IdeaNode]

class BrainstormerOutput(BaseModel):
    ideas: List[IdeaNode] = Field(
        description=f"Propose {MIN_NEW_IDEA_COUNT}-{MAX_NEW_IDEA_COUNT} exclusive technical strategies.",
        min_length=MIN_NEW_IDEA_COUNT,
        max_length=MAX_NEW_IDEA_COUNT
    )

def brainstormer(state: ThinkerState):
    """
    Proposes new ideas based on the problem statement, current code, and past failures (history).
    """
    history = "\n".join([f"- {h}" for h in state.history])
    
    user_prompt = clean_docstring(f"""
    <goal>
    {state.problem_statement}
    </goal>
    <Current Code>
    {state.current_code}
    </Current Code>
    <improvement_scope>
    {state.improvement_scope}
    </improvement_scope>
    """)

    structured_llm = llm.with_structured_output(BrainstormerOutput)

    response = structured_llm.invoke([
        SystemMessage(content=BRAINSTORM_SYSTEM_PROMPT.format(history=history, MIN_NEW_IDEA_COUNT=MIN_NEW_IDEA_COUNT, MAX_NEW_IDEA_COUNT=MAX_NEW_IDEA_COUNT)),
        HumanMessage(content=user_prompt)
    ])
    
    # Add new ideas to the global pool for the UI/Comparator to see
    return {"candidate_ideas": state.candidate_ideas + response.ideas}
