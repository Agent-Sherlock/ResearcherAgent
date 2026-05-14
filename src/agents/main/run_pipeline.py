from src.agents.main.graph import get_main_graph

def run_pipeline(problem_statement: str, initial_code: str = "") -> dict:
    graph = get_main_graph()
    
    # Initialize the GlobalState
    initial_state = {
        "problem_statement": problem_statement,
        "current_code": initial_code,
        "current_best_score": 0.0,
        "history": [],
        "candidate_ideas": []
    }
    
    result = graph.invoke(initial_state)
    return result