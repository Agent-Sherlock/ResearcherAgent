"""
arena_creator.py

Uses LangChain + OpenRouter + structured output to generate `solution.py`
and `verifier.py` from a research goal. No agent loop, just one LLM call.

Expects:
- prompts.py in the same package (exports `build_prompt`)
- src.shared.client.openrouter_api_key()
- src.config.config.BASE_DIRECTORY, GIT_REPO_PATH
"""

import asyncio
from pathlib import Path
from typing import Optional

from pydantic import BaseModel, Field

from .prompts import build_prompt
from src.shared.client import openrouter_api_key
from src.config.config import BASE_DIRECTORY, GIT_REPO_PATH
from src.shared.client import CREATE_ARENA_CLIENT
from src.shared.utils.general_utils import clean_docstring

# ---- Pydantic model for structured output ----
class ArenaFiles(BaseModel):
    solution_py: str = Field(description="Complete code for solution.py")
    verifier_py: str = Field(description="Complete code for verifier.py")
    improvement_scope: str = Field(
        description=clean_docstring("Description of what parts of solution.py the AI researcher is allowed to modify "
                    "(e.g., 'model architecture and optimizer hyperparameters, but not the training loop "
                    "or the input/output signature'). Should be a short, clear sentence.")
    )


async def create_arena(
    user_goal: str,
    title: str
) -> dict[str, Path]:
    """
    Generate and write the two arena files.
    Returns dict mapping filename (solution.py, verifier.py) to the written Path.
    """
    # Workspace directory
    workspace = Path(BASE_DIRECTORY) / GIT_REPO_PATH / title
    workspace.mkdir(parents=True, exist_ok=True)

    # Attach structured output to the model
    structured_model = CREATE_ARENA_CLIENT.with_structured_output(ArenaFiles)

    # One-shot prompt (unchanged from your prompts.py)
    prompt_text = build_prompt(user_goal)

    # Call – run blocking I/O in a thread to keep the async event loop free
    result: ArenaFiles = await asyncio.to_thread(
        structured_model.invoke, prompt_text
    )

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
        path.write_text(code, encoding="utf-8")
        written[name] = path
        print(f"✅ {path}")

    return written