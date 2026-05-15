import asyncio
from pathlib import Path
from typing import Optional
import subprocess
from src.config.config import BASE_DIRECTORY, GIT_REPO_PATH
from pydantic import BaseModel, Field

from .prompts import build_prompt
from src.shared.client import openrouter_api_key
from src.config.config import BASE_DIRECTORY, GIT_REPO_PATH
from src.shared.client import CREATE_ARENA_CLIENT
from src.shared.utils.general_utils import clean_docstring
from src.agents.main.state import GlobalState
from src.shared.utils.git_tool import write_to_file

class ArenaFiles(BaseModel):
    solution_py: str = Field(description="Complete code for solution.py")
    verifier_py: str = Field(description="Complete code for verifier.py")
    improvement_scope: str = Field(
        description=clean_docstring("Description of what parts of solution.py the AI researcher is allowed to modify "
                    "(e.g., 'model architecture and optimizer hyperparameters, but not the training loop "
                    "or the input/output signature'). Should be a short, clear sentence.")
    )


def _create_arena(
    user_goal: str,
    title: str
) -> dict[str, Path]:
    """
    Generate and write the two arena files.
    Returns dict mapping filename (solution.py, verifier.py) to the written Path.
    """
    # Workspace directory
    workspace = (Path(BASE_DIRECTORY) / GIT_REPO_PATH / title).resolve()

    # Attach structured output to the model
    structured_model = CREATE_ARENA_CLIENT.with_structured_output(ArenaFiles)

    # One-shot prompt (unchanged from your prompts.py)
    prompt_text = build_prompt(user_goal)

    # Call – run blocking I/O in a thread to keep the async event loop free
    result: ArenaFiles = structured_model.invoke(prompt_text)

    print("-" * 20)
    print("generated improvement_scope: ")
    print(result.improvement_scope)
    print("-" * 20)

    # Write files
    written = {}
    for name, code in [
        ("solution.py", result.solution_py),
        ("verifier.py", result.verifier_py),
    ]:
        path = workspace / name
        write_to_file(path, code)
        written[name] = path
        print(f"✅ {path}")

    return result

def create_arena(
    state: GlobalState
) -> dict:
    title = state.git_repo_name

    arena_result = _create_arena(
        user_goal=state.problem_statement,
        title=title
    )

    # run the code to make sure it works and get the initial score
    workspace = (BASE_DIRECTORY / GIT_REPO_PATH / title).resolve()
    python_exe = r"C:\Users\lotan\AppData\Local\Programs\Python\Python312\python.exe"

    result = subprocess.run(
        [python_exe, "verifier.py"],
        cwd=str(workspace),
        capture_output=True,
        text=True
    )

    try:
        stdout = result.stdout.strip()
        stdout_float = float(stdout)
        print("STDOUT:", stdout_float)
    except Exception as e:
        print("Error reading STDOUT:", e)
        print("STDERR:", result.stderr.strip())
        exit()

    return {
        "current_code": arena_result.solution_py,
        "current_best_score": stdout_float,
        "improvement_scope": arena_result.improvement_scope
    }
