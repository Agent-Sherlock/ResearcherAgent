from typing import Literal
from langgraph.graph import StateGraph, START, END
from src.agents.thinker.state import ThinkerState

from src.agents.thinker.nodes.brainstormer import brainstormer
from src.agents.thinker.nodes.selector import comparator

def should_continue_thinking(state: ThinkerState) -> Literal["brainstormer", END]:
    if not state.candidate_ideas:
        return "brainstormer"
    return END

def get_thinker_graph():
    thinker_builder = StateGraph(ThinkerState)

    thinker_builder.add_node("brainstormer", brainstormer)
    thinker_builder.add_node("comparator", comparator)

    thinker_builder.add_edge(START, "brainstormer")
    thinker_builder.add_edge("brainstormer", "comparator")

    thinker_builder.add_conditional_edges(
        "comparator",
        should_continue_thinking
    )

    thinker_subgraph = thinker_builder.compile()

    return thinker_subgraph