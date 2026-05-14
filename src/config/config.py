"""
the python config file for the agent, where we set up "hyperparameters" like which LLM to use, how many ideas to generate, etc.
"""
import pathlib

RANDOM_SEED = 42
GIT_REPO_PATH = "data/history"

MIN_NEW_IDEA_COUNT = 3
MAX_NEW_IDEA_COUNT = 6

BASE_DIRECTORY = pathlib.Path(__file__).parent.parent.parent.resolve()
