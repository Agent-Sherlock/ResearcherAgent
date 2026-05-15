import sys

from src.shared.utils.git_tool import git_commit_to_branch, git_read_file_from_commit, git_get_history, write_to_file
from src.agents.main.state import GlobalState
from src.config.config import BASE_DIRECTORY, GIT_REPO_PATH
from src.shared.utils import logger as log

import subprocess
from pathlib import Path


def checker_execute(state: GlobalState) -> dict:
    repo_path = Path(BASE_DIRECTORY / GIT_REPO_PATH / state.git_repo_name).resolve()
    title = state.git_repo_name
    workspace = (BASE_DIRECTORY / GIT_REPO_PATH / title).resolve()
    python_exe = "python"

    result = subprocess.run(
        [python_exe, "verifier.py"],
        cwd=str(workspace),
        capture_output=True,
        text=True
    )

    try:
        stdout = result.stdout.strip()
        stdout_float = float(stdout)
        log.info(f"STDOUT: {stdout_float}")
    except Exception as e:
        log.error(f"Error reading STDOUT: {e}")
        log.error(f"STDERR: {result.stderr.strip()}")
        log.info(f"Score did not improve: {stdout_float} (current best: {state.current_best_score})")
        return {}
        
    if stdout_float > state.current_best_score: # commit the code, its good!
        state_file_path = workspace / "state.json"
        
        # Serialize state (supports both Pydantic v1 and v2)
        state_json = state.model_dump_json(indent=4) if hasattr(state, "model_dump_json") else state.json(indent=4)
        
        write_to_file(str(state_file_path), state_json)

        log.info(f"New best score: {stdout_float} (previous: {state.current_best_score})")
        git_commit_to_branch(workspace, title)
        hash_codes = git_get_history(repo_path)
        hash_code = hash_codes["hashes"][0]  # get the latest commit hash
        file_res = git_read_file_from_commit(workspace, hash_code, "solution.py")
        new_code = file_res["content"]

        return {
            "current_best_score": stdout_float,
            "current_code": new_code, 
            "history": []
            }
    else:
        # add to history
        log.info(f"Score did not improve: {stdout_float} (current best: {state.current_best_score})")
        return {
            "history": state.history + [state.candidate_ideas[0].title],
            "iteration_count": state.iteration_count + 1
        }

