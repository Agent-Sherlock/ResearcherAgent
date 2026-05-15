def build_prompt(user_goal: str) -> str:
    return f"""You are an Expert Benchmark Engineer.
Your ONLY job is to create an evaluation arena for an AI Autoresearcher.
You do NOT improve the solution; you just produce the STARTING BASELINE and a VERIFIER.

The research goal is:
<GOAL>
{user_goal}
</GOAL>

Produce EXACTLY TWO files. No other text, no explanations, no markdown outside the files.

FILE 1: `solution.py`
- This is the baseline implementation. It must be CORRECT but MINIMAL.
- It must expose a clear entry point: a function, class, or pipeline that performs the core task.
- It MUST NOT contain evaluation logic, metric calculations, or test datasets.
- Keep it as simple as possible (e.g., a single file with minimal dependencies).
- For **machine-learning tasks** (image classification, NLP, etc.): 
  * The file must contain the model definition and a function `create_model() -> nn.Module` that returns an instantiated model.
  * It must also define a function `create_optimizer(model: nn.Module) -> torch.optim.Optimizer` that returns an optimizer instance configured for the model (e.g., Adam with a chosen learning rate).
  * The model must be **minimal but credible** - e.g., a two-layer MLP with a non-linearity (ReLU) for MNIST and a .
  * Do NOT include any training loop, data loading, or loss calculation. The verifier will handle all training, using your model and optimizer.

FILE 2: `verifier.py`
- This is a STATELESS evaluator. It does NOT read or write any files except `solution.py` (for importing).
- It must define a function `run_benchmark() -> float` that:
  1. Dynamically imports the entry point from `solution.py`.
  2. Creates a **challenging, realistic test scenario** appropriate for the goal:
     - For **speed benchmarks** (e.g., matrix multiplication, sorting):
        * Use **large inputs** (e.g., 200x200 matrices).
        * **The test data must be randomly generated** - do NOT use constant values. Use appropriate libraries like `random`, `numpy.random`, etc.
        * Set a fixed random seed (e.g., `random.seed(42)`) at the start of `run_benchmark()` for reproducibility.
        * Measure average execution time over multiple trials.
     - For **machine-learning tasks** (e.g., “Train an MNIST classifier”):
        * The verifier OWNs the training loop entirely. It must:
          - Call `solution.create_model()` to get the model.
          - Set up the dataset (e.g., MNIST via `torchvision`), data loaders, loss function (e.g., `CrossEntropyLoss`), and call the optimizer (e.g., `Adam`) from the solution. Do judgment to make the training non-trivial but not excessively long. 
          - Train the model for a **fixed time budget** (e.g., `TRAINING_TIME_SECONDS = 35`). Use `time.time()` to stop training exactly after that many seconds, irrespective of epoch count.
          - After training, evaluate the model on the test set and compute **accuracy** as a float (0-100).
          - Return that accuracy.
        * The time budget MUST be a clearly named constant at the top of the file (e.g., `TRAINING_TIME_BUDGET = 120`).
        * Use a fixed random seed (`torch.manual_seed(42)`) for reproducible data splits/initialisation.
        * Do NOT modify `solution.py`; only call `solution.create_model()`.
     - For other domains, infer a meaningful, reproducible evaluation harness.
  3. Returns a **single float** representing the metric (execution time, accuracy, loss, etc.).
  4. **Must import all libraries it uses** for test data generation or training (e.g., `import torch`, `import torch.nn as nn`, `from torchvision import datasets, transforms`). Assume they are already installed - do **not** try to install them.
- When run as a script (`if __name__ == "__main__"`):
  - Call `run_benchmark()` and print its return value to stdout (nothing else, no labels, no formatting - just `print(run_benchmark())`).
  - If an exception occurs, print the error message to **stderr** and exit with a non-zero code. Do **not** print anything to stdout in that case.
- The verifier must **never** read `best_score.txt`, write any file, or copy `solution.py`. It is a pure evaluation tool.

IMPORTANT:
- You are returning data through a structured JSON schema. The JSON object must have exactly two keys: "solution_py" and "verifier_py".
- Place the RAW Python code directly into those fields as plain strings. Do NOT wrap them in markdown code blocks (do not use ```python or ```).
- Do NOT add any extra commentary, explanations, greetings, or other text. Output only the JSON object.

ADDITIONAL FIELD:
- Also return a key "improvement_scope" containing a short description of what the Autoresearcher is allowed to modify in `solution.py`.
- The description must be **permissive**: the agent may change any part of the code (algorithm, architecture, optimizer, hyperparameters, internal helper functions, etc.), as long as the **entry points expected by the verifier remain intact**.  
- Specifically, the verifier imports these from `solution.py`: [list the exact function/class names the verifier uses, e.g., `create_model`, `create_optimizer`]. Those names (and their required arguments/return types) must stay the same, but the agent can freely change their implementation or add new functions.
- Example for an MNIST goal: “You can modify the model architecture, optimizer type, learning rate, and any internal details. The verifier expects `create_model()` returning an `nn.Module` and `create_optimizer(model)` returning a `torch.optim.Optimizer`. Do not change those function signatures.”
- Example for a matrix multiplication goal: “You can change the multiplication algorithm or use libraries. The verifier expects a function `matrix_multiply(A, B)` that returns the product. Keep that signature, but everything else is modifiable.”
- Keep the scope concise (1-2 sentences).
"""

