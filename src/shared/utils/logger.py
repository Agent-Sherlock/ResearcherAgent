import logging
import os
from datetime import datetime

class Logger:
    def __init__(self, name="logger", active=True):
        self.active = active

        if not self.active:
            self.log_dir = None
            return

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_dir = os.path.join("data", "logs")
        os.makedirs(self.log_dir, exist_ok=True)
        log_path = os.path.join(self.log_dir, f"{name}_{timestamp}.txt")

        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            handlers=[
                logging.FileHandler(log_path, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )

        self.info("Logger initialized. Logs will be saved to: %s", log_path)
    
    def info(self, *args, **kwargs):
        if self.active:
            logging.info(*args, **kwargs)
    
    def warning(self, *args, **kwargs):
        if self.active:
            logging.warning(*args, **kwargs)
    
    def print_start_end(self, message: str, code: str, num_chars: int = 200):
        if self.active:
            preview = (code[:num_chars] + "..." + code[-num_chars:]) if len(code) > num_chars*2 else code
            logging.info(f"{message}:\n{preview}")

    def get_path(self):
        # Return the base path of the current log directory
        return self.log_dir if self.active else None
    
    def error(self, *args, **kwargs):
        if self.active:
            logging.error(*args, **kwargs)
    
    def exception(self, *args, **kwargs):
        if self.active:
            logging.exception(*args, **kwargs)


logger = Logger()