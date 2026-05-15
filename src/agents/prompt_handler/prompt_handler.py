from src.agents.main.state import GlobalState
from src.shared.client import CHEAP_CLIENT
from src.shared.utils.general_utils import clean_docstring
from src.shared.utils.logger import logger
from src.config.config import BASE_DIRECTORY, GIT_REPO_PATH
from src.shared.utils.git_tool import git_create_repo

import uuid
from pydantic import BaseModel, Field

class PromptHandlerOutput(BaseModel):
    refined_prompt: str = Field(description="Rephrase the prompt to be assertive, e.g: Instead of 'please create me a good neural network for classifying images of cats vs dogs', say 'Train a Neural Network classifier with amazing accuracy using PyTorch to classify images of cats and dogs.'")
    title: str = Field(description="Title for the said problem, should be short and descriptive, e.g. 'Cat vs Dog Classifier', less than 8 words.")

system_msg = (
    "You are an expert at rephrasing research goals. "
    "Convert the user's vague request into an assertive, imperative instruction "
    "and give a short, descriptive project title."
)

def handle_prompt(state: GlobalState) -> dict:
    # step 1: generate the title.
    structured_model = CHEAP_CLIENT.with_structured_output(PromptHandlerOutput)
    
    result: PromptHandlerOutput = structured_model.invoke(
        f"{system_msg}\n\nUser request: {state.problem_statement}"
    )

    refined_prompt = result.refined_prompt
    title = result.title

    cleaned_title = "".join(c if c.isalnum() else "_" for c in title).strip("_")[:50] + "_" + str(uuid.uuid4().hex[:8])
    safe_dirname = f"{cleaned_title}_{uuid.uuid4().hex[:8]}"

    # log the results for debugging
    logger.info("Refined prompt: %s", refined_prompt)
    logger.info("Generated title: %s", title)
    logger.info("Cleaned title: %s", cleaned_title)
    logger.info("Safe directory name: %s", safe_dirname)

    # step 2: generate the git repo path. 
    git_path = (BASE_DIRECTORY / GIT_REPO_PATH / safe_dirname).resolve()
    git_create_repo(git_path)

    # step 3: return output to new state
    return {
        "problem_statement": refined_prompt,
        "git_repo_name": safe_dirname
    }
