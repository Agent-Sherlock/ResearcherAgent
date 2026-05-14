"""
ensures the .env file exists, and if so that the api key(s) in it are valid. 
"""

from src.config.init_env import ensure_env_vars
from src.shared.utils.logger import logger as log

import requests

def validate_clients():
    try:
        from src.shared.client import THINKER_CLIENT, SELECTOR_CLIENT

        THINKER_CLIENT.invoke("answer this response in only one word: are you working?")
        SELECTOR_CLIENT.invoke("answer this response in only one word: are you working?")

        log.info("OPENROUTER clients are responsive.")
    except requests.exceptions.HTTPError as e:
        error_msg = str(e)[:100]
        log.error(f"HTTP error during validation: {error_msg}")
        exit()
    except Exception as e:
        error_msg = str(e)[:100]
        log.error(f"API validation failed. Error: {error_msg}")
        exit()

def validate_workspace():
    ensure_env_vars()
    validate_clients()
