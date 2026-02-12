# logger/custom_logger.py
import os
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime
import traceback
import sys
import structlog


class CustomLogger:
    """
    Structured JSON logger with rotating file support.
    Automatically captures exceptions and includes file name and line number
    from custom exceptions if present.
    """

    def __init__(self, log_dir="logs", max_bytes=5_000_000, backup_count=5):
        self.logs_dir = os.path.join(os.getcwd(), log_dir)
        os.makedirs(self.logs_dir, exist_ok=True)

        self.log_file_path = os.path.join(self.logs_dir, "document_portal.log")
        self.max_bytes = max_bytes
        self.backup_count = backup_count

    def get_logger(self, name):
        logger_name = os.path.basename(name)

        # ---------- stdlib logger ----------
        std_logger = logging.getLogger(logger_name)
        std_logger.setLevel(logging.DEBUG)

        #if not std_logger.handlers:
        # CLEAR EXISTING HANDLERS
        std_logger.handlers.clear()
         # Rotating file handler
        file_handler = RotatingFileHandler(
        self.log_file_path,
        maxBytes=self.max_bytes,
        backupCount=self.backup_count,
        mode="a",
        encoding="utf-8",
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(logging.Formatter("%(message)s"))
        std_logger.addHandler(file_handler)

        # Console handler (optional)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(logging.Formatter("%(message)s"))
        std_logger.addHandler(console_handler)

        std_logger.propagate = False

        # ---------- structlog processors ----------
        def enrich_exception(event_logger, method_name, event_dict):
            """
            Attach exception traceback and, if a custom exception is logged,
            include its file_name and lineno automatically.
            """
            exc_type, exc_value, exc_tb = sys.exc_info()
            if exc_tb is not None:
                # Always attach traceback
                event_dict["exception"] = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))

                # If the exception is a DocumentPortalException, include extra fields
                if hasattr(exc_value, "file_name") and hasattr(exc_value, "lineno"):
                    event_dict["file_name"] = getattr(exc_value, "file_name", "Unknown")
                    event_dict["lineno"] = getattr(exc_value, "lineno", -1)

            return event_dict

        structlog.configure(
            processors=[
                structlog.processors.TimeStamper(fmt="iso", utc=True, key="timestamp"),
                structlog.processors.add_log_level,
                enrich_exception,  # auto-attach exception + file/line info
                structlog.processors.JSONRenderer(),
            ],
            logger_factory=structlog.stdlib.LoggerFactory(),
            wrapper_class=structlog.stdlib.BoundLogger,
            cache_logger_on_first_use=True,
        )

        return structlog.get_logger(logger_name)
