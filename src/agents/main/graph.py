from src.agents.thinker.thinker import think
from src.agents.main.state import GlobalState
from src.agents.arena_coder.arena_coder import create_arena
from src.agents.prompt_handler.prompt_handler import handle_prompt
from src.agents.coder.coder_node import coder_agent
from src.agents.checker.checker import checker_execute

from langgraph.graph import StateGraph, START, END

def get_main_graph():
    builder = StateGraph(GlobalState)
    builder.add_node("create_arena", create_arena)
    builder.add_node("thinker", think)
    builder.add_node("handle_prompt", handle_prompt)
    builder.add_node("coder_agent", coder_agent)
    builder.add_node("checker", checker_execute)

    builder.add_edge(START, "handle_prompt")
    builder.add_edge("handle_prompt", "create_arena")
    builder.add_edge("create_arena", "thinker")
    builder.add_edge("thinker", "coder_agent")
    builder.add_edge("coder_agent", "checker")
    builder.add_edge("checker", END)

    return builder.compile()