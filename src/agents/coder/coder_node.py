import os

from openhands.sdk import LLM, Agent, Conversation, ConversationExecutionStatus, Tool
from openhands.tools.file_editor import FileEditorTool
from openhands.tools.task_tracker import TaskTrackerTool

from src.shared.client import CODER_CLIENT as llm
from src.agents.main.state import GlobalState
from src.config.config import BASE_DIRECTORY, GIT_REPO_PATH
from src.shared.utils.logger import logger as log
from src.agents.coder.prompts import task_instruction
from src.shared.utils.logger import logger

def coder_agent(state: GlobalState) -> dict:
    current_code = state.current_code
    problem_statement = state.problem_statement
    candidate_idea_node = state.candidate_ideas[0]
    candidate_idea = candidate_idea_node.details

    target_file_path = os.path.join(BASE_DIRECTORY, GIT_REPO_PATH, state.git_repo_name, "solution.py")

    instruction = task_instruction.format(
        problem_statement=problem_statement,
        candidate_idea=candidate_idea,
        current_code=current_code,
        target_file_path=target_file_path, 
        improvement_scope=state.improvement_scope
    )

    logger.info(f"Coder Agent received task instruction:\n{instruction}")
    tools = [
        Tool(name=FileEditorTool.name),
        Tool(name=TaskTrackerTool.name)
    ]
    
    agent = Agent(llm=llm, tools=tools)
    
    conversation = Conversation(agent=agent, workspace=BASE_DIRECTORY)
    
    conversation.send_message(instruction)
    conversation.run()

    logger.info(f"Conversation with coder finished with status: {conversation.state.execution_status}")

    if conversation.state.execution_status == ConversationExecutionStatus.FINISHED:
        return {}
    else:
        logger.error("Coder agent failed to complete the task.")
        exit()