import os
import logging
from datetime import datetime
import structlog
import sys
import traceback

class CustomLogger:
    """
    Structured JSON logger that auto-captures exceptions
    without passing exc_info=True.
    """

    def __init__(self, log_dir="logs"):
        self.logs_dir = os.path.join(os.getcwd(), log_dir)
        os.makedirs(self.logs_dir, exist_ok=True)

        log_file = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
        self.log_file_path = os.path.join(self.logs_dir, log_file)

    def get_logger(self, name):
        logger_name = os.path.basename(name)

        # Standard logging setup
        std_logger = logging.getLogger(logger_name)
        std_logger.setLevel(logging.ERROR)
   # Configure logging for file 
        if not std_logger.handlers:
            file_handler = logging.FileHandler(self.log_file_path, mode="a")
            file_handler.setLevel(logging.ERROR)
            file_handler.setFormatter(logging.Formatter("%(message)s"))
            std_logger.addHandler(file_handler)
   # Configure logging for console 
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.ERROR)
            console_handler.setFormatter(logging.Formatter("%(message)s"))
            std_logger.addHandler(console_handler)

            logging.basicConfig(
                level=logging.INFO,
                format="%(message)s",  # Structlog will handle JSON rendering
                handlers=[console_handler, file_handler]
            )
            std_logger.propagate = False

        # Structlog processors
        def inject_active_exception(logger, method_name, event_dict):
            """
            If there is an active exception, attach its traceback to event_dict
            """
            exc_type, exc_value, exc_tb = sys.exc_info()
            if exc_tb is not None:
                event_dict["exception"] = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
            return event_dict

        structlog.configure(
            processors=[
                structlog.processors.TimeStamper(fmt="iso", utc=True, key="timestamp"),
                structlog.processors.add_log_level,
                inject_active_exception,  # auto attach active exception
                structlog.processors.JSONRenderer(),
            ],
            logger_factory=structlog.stdlib.LoggerFactory(),
            wrapper_class=structlog.stdlib.BoundLogger,
            cache_logger_on_first_use=True,
        )

        return structlog.get_logger(logger_name)



## --- Usage Example ---
if __name__ == "__main__":

    logger = CustomLogger().get_logger(__file__)
    logger.info("User uploaded a file", user_id=123, filename="report.pdf")
    logger.error("Failed to process PDF", error="File not found", user_id=123)