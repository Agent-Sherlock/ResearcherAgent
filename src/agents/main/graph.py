from src.agents.thinker.thinker import think
from src.agents.main.state import GlobalState
from src.agents.arena_coder.arena_coder import create_arena

from langgraph.graph import StateGraph, START, END

def get_main_graph():
    builder = StateGraph(GlobalState)
    builder.add_node("create_arena", create_arena)
    builder.add_node("thinker", think)

    builder.add_edge(START, "create_arena")
    builder.add_edge("create_arena", "thinker")
    builder.add_edge("thinker", END)
    
    return builder.compile()