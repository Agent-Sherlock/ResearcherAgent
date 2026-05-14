import os
from pathlib import Path

from src.shared.utils.logger import logger as logger

ENV_FILE = Path(__file__).resolve().parent.parent.parent / '.env'
REQUIRED_VARS = ['OPENROUTER_API_KEY'] # add more requirements as needed. 

def ensure_env_vars():
    created = False
    updated = False
    env_vars = {}
    
    # Read existing .env if it exists
    if os.path.exists(ENV_FILE):
        with open(ENV_FILE, 'r') as f:
            for line in f:
                if '=' in line:
                    key, value = line.strip().split('=', 1)
                    env_vars[key] = value
    else:
        created = True
        with open(ENV_FILE, 'w') as f:
            pass  # Create empty .env
        logger.info("Created new %s file.", ENV_FILE)

    # Check and add missing variables
    with open(ENV_FILE, 'a') as f:
        for var in REQUIRED_VARS:
            if var not in env_vars:
                f.write(f'{var}=\n')
                logger.info("Added missing variable: %s", var)
                updated = True

    if not created and not updated:
        logger.info("All required variables already exist in %s.", ENV_FILE)
    else:
        logger.info("Please fill in the required variables in %s before running the agent.", ENV_FILE)
        exit()

if __name__ == "__main__":
    ensure_env_vars()
