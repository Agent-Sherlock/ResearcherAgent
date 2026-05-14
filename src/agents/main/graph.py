from src.agents.thinker.thinker import think
from src.agents.main.state import GlobalState
from langgraph.graph import StateGraph, START, END

def get_main_graph():
    builder = StateGraph(GlobalState)
    
    builder.add_node("thinker", think)
    builder.add_edge(START, "thinker")
    builder.add_edge("thinker", END)
    
    return builder.compile()