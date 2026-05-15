import os
from pathlib import Path

from langchain_openrouter import ChatOpenRouter
from openhands.sdk import LLM
from langchain_core.rate_limiters import InMemoryRateLimiter
from src.config.config import RANDOM_SEED


def openrouter_api_key() -> str:
    key = os.getenv("OPENROUTER_API_KEY")
    if key:
        return key
    env_file = Path(__file__).resolve().parent.parent.parent / ".env"
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            if line.startswith("OPENROUTER_API_KEY="):
                return line.split("=", 1)[1].strip()
    raise KeyError("OPENROUTER_API_KEY")

rate_limiter = InMemoryRateLimiter(
    requests_per_second=1,
    check_every_n_seconds=0.5,
    max_bucket_size=2
)

THINKER_CLIENT = ChatOpenRouter(
    model="deepseek/deepseek-v4-flash",
    temperature=1.2,
    api_key=openrouter_api_key(),
    seed=RANDOM_SEED
)

SELECTOR_CLIENT = ChatOpenRouter(
    model="deepseek/deepseek-v4-flash",
    temperature=0,
    api_key=openrouter_api_key(),
    seed=RANDOM_SEED
)

CREATE_ARENA_CLIENT = ChatOpenRouter(
    model="qwen/qwen3-coder-30b-a3b-instruct",
    temperature=0,
    api_key=openrouter_api_key(),
    seed=RANDOM_SEED, 
    max_tokens=4096,
)

CODER_CLIENT = LLM(
    model="openrouter/qwen/qwen3-coder-30b-a3b-instruct",
    api_key=openrouter_api_key(),
    base_url="https://openrouter.ai/api/v1",
    temperature=0,
)

CHEAP_CLIENT = ChatOpenRouter(
    model="qwen/qwen3-coder-30b-a3b-instruct",
    temperature=0,
    api_key=openrouter_api_key(),
    seed=RANDOM_SEED
)

