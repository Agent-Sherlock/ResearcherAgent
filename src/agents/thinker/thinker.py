from src.agents.main.state import GlobalState
from src.agents.thinker.graph import get_thinker_graph

_thinker_subgraph = get_thinker_graph()

def think(state: GlobalState) -> dict:
    """Invokes the thinker subgraph natively."""

    sub_input = {
        "problem_statement": state.problem_statement,
        "current_code": state.current_code,
        "history": state.history,
        "improvement_scope": state.improvement_scope,
        "candidate_ideas": [] # reset ideas for now (as they may not be relavent after the first iteration)
    }

    return _thinker_subgraph.invoke(sub_input)
