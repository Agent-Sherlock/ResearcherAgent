from src.agents.main.state import GlobalState
from src.agents.thinker.graph import get_thinker_graph
from src.shared.utils import logger as log

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

    result = _thinker_subgraph.invoke(sub_input)

    log.info(f"Thinker proposed: {result.get('candidate_ideas', [])}")

    return result
