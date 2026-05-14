import os

from openhands.sdk import LLM, Agent, Conversation, ConversationExecutionStatus, Tool
from openhands.tools.file_editor import FileEditorTool
from openhands.tools.task_tracker import TaskTrackerTool
from src.shared.client import CODER_CLIENT as llm
from src.agents.main.state import GlobalState
from src.config.config import BASE_DIRECTORY
from src.shared.utils.logger import logger as log


async def coder_agent(state: GlobalState):
    current_code = state.current_code
    problem_statement = state.problem_statement
    candidate_idea_node = state.candidate_ideas[0]
    candidate_idea = candidate_idea_node.details
    # TODO - get the exact file path from GlobalState
    target_file_path = os.path.join(BASE_DIRECTORY, "data", "history", "1", "main.py")    
    task_instruction = f"""
    You are an expert developer. Your task is to implement a solution based on the provided idea.
    Problem Statement:
    {problem_statement}
    Candidate Idea to Implement:
    {candidate_idea}
    Current Code Context:
    {current_code}
    Instructions:
    1. Write the code to implement the candidate idea.
    2. You MUST edit the existing file at {target_file_path} using the str_replace command. Do not create a new file:
       {target_file_path}
    """
    log.info(f"Coder Agent received task instruction:\n{task_instruction}")
    tools = [
        Tool(name=FileEditorTool.name),
        Tool(name=TaskTrackerTool.name)
    ]
    
    agent = Agent(llm=llm, tools=tools)
    
    conversation = Conversation(agent=agent, workspace=BASE_DIRECTORY)
    
    conversation.send_message(task_instruction)
    conversation.run()
    if conversation.state.execution_status == ConversationExecutionStatus.FINISHED:
        return True
    return False