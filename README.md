# Agent-Sherlock

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## The Idea Behind the Project

In software and research, we often encounter complex problems with no immediate or obvious solutions. Agent-Sherlock tackles this by utilizing an iterative LangGraph loop to enable the system to learn from its past mistakes and continuously generate better solutions.

Think of it as a form of Machine Learning, but without neural networks. Instead of updating numerical weights, the system updates its reasoning, architecture, and code implementations over successive generations by takeing successive steps ang ignoring and avoiding previous mistakes.

## Project Structure

```
Agent-Sherlock/
├── LICENSE
├── main.py
├── README.md
├── requirements.txt
├── test.py
├── data/
│   ├── history/
│   │   └── 1/
│   │       └── main.py
│   └── logs/
│       └── (log files)
├── src/
│   ├── agents/
│   │   ├── arena_coder/
│   │   │   ├── arena_coder.py
│   │   │   └── prompts.py
│   │   ├── checker/
│   │   │   └── checker.py
│   │   ├── coder/
│   │   │   ├── coder_node.py
│   │   │   └── prompts.py
│   │   ├── main/
│   │   │   ├── graph.py
│   │   │   ├── run_pipeline.py
│   │   │   ├── state.py
│   │   │   └── nodes/
│   │   │       └── thinker.py
│   │   ├── prompt_handler/
│   │   │   └── prompt_handler.py
│   │   └── thinker/
│   │       ├── graph.py
│   │       ├── prompts.py
│   │       ├── state.py
│   │       ├── thinker.py
│   │       └── nodes/
│   │           ├── brainstormer.py
│   │           └── selector.py
│   ├── config/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── Dockerfile
│   │   ├── init_env.py
│   │   └── validate_workspace.py
│   └── shared/
│       ├── client.py
│       └── utils/
│           ├── __init__.py
│           ├── general_utils.py
│           ├── git_tool.py
│           └── logger.py
```

Here is a breakdown of the core components of the system:

### Core Agents (src/agents/)

#### main/ (Orchestrator)
- `graph.py` / `run_pipeline.py`: Defines the main LangGraph state machine that connects all sub-agents in a continuous improvement loop.
- `state.py`: Holds the global state of the application (current code, best score, iteration count, and history of past failures).

#### prompt_handler/
- `prompt_handler.py`: Takes the user's initial vague request, refines it into a strict assertive instruction, and sets up a safe, isolated Git repository for the experiment.

#### arena_coder/
- `arena_coder.py` / `prompts.py`: Creates the "Evaluation Arena." It generates a minimal starting baseline (`solution.py`) and a stateless evaluator (`verifier.py`) to benchmark future improvements.

#### thinker/
- `thinker.py` / `graph.py`: A sub-graph dedicated to reasoning.
- `nodes/brainstormer.py`: Analyzes the problem and past failures to propose 3-6 new, distinct technical strategies.
- `nodes/selector.py`: Acts as a tech lead, evaluating and scoring the proposed ideas to select the most viable one for implementation.

#### coder/
- `coder_node.py`: Utilizes the OpenHands framework to edit the codebase. It takes the chosen idea and safely modifies the existing `solution.py`.

#### checker/
- `checker.py`: Runs the verifier against the newly generated code. If the code improves the benchmark score, it commits the changes via Git. Otherwise, it logs the failure to the history so the Thinker avoids repeating the mistake.

### Configuration & Utils (src/config/ & src/shared/)

- `config/config.py` & `init_env.py`: Handles hyperparameters (idea counts, random seeds) and ensures the environment (.env) is correctly set up.
- `config/validate_workspace.py`: Validates that the necessary API keys are present and the LLM clients are responsive.
- `shared/client.py`: Configures the various LLM clients (OpenRouter, DeepSeek, Qwen) with rate limiting and specific model parameters.
- `shared/utils/git_tool.py`: A robust wrapper around Git commands to manage version control, track histories, and pull specific file versions from past commits.
- `shared/utils/logger.py`: A custom logging utility that tracks the agent's progress and saves logs to the `data/logs/` directory.

## Tools & Libraries Used

- **LangGraph**: Manages the cyclical flow of states and agent interactions (the core loop).
- **LangChain & langchain-openrouter**: Orchestrates LLM calls and structured outputs.
- **OpenHands SDK**: Powers the coder_agent with file-editing capabilities.
- **Pydantic**: Ensures robust, structured JSON outputs from the LLMs.
- **Git (via Python subprocess)**: Used natively to maintain version control of the experiments, allowing the system to revert or branch from successful states.

## Getting Started

### 1. Install Requirements

Make sure you have Python installed, then install the required dependencies:

```bash
pip install -r requirements.txt
```

### 2. Environment Setup

The system requires an OpenRouter API key. When you run the system for the first time, it will automatically generate an empty `.env` file for you if one does not exist.

Fill in your API key in the `.env` file:

```
OPENROUTER_API_KEY=your_api_key_here
```

