# logger/custom_exception.py
import sys
import traceback

from logger.custom_logger_archive import CustomLogger
logger=CustomLogger().get_logger(__file__)


class DocumentPortalException(Exception):
    """
    Custom exception that stores traceback, filename, and line number.
    """

    def __init__(self, error_message: Exception):
        super().__init__(error_message)

        exc_type, exc_value, exc_tb = sys.exc_info()
        if exc_tb:
            self.file_name = exc_tb.tb_frame.f_code.co_filename
            self.lineno = exc_tb.tb_lineno
        else:
            self.file_name = "Unknown"
            self.lineno = -1

        self.error_message = str(error_message)
        self.traceback_str = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))

    def __str__(self):
        return f"""
        Error in [{self.file_name}] at line [{self.lineno}]
        Message: {self.error_message}
        Traceback:
        {self.traceback_str}
"""


### Testing Exceptions logging    
if __name__ == "__main__":
    try:
        # Simulate an error
        a = 1 / 0
    except Exception as e:
        app_exc = DocumentPortalException(e)

    # ✅ auto logs traceback without exc_info=True
        logger.info("Document Portal error occurred")

    # Preserve original traceback if needed
        print("exception details from except block ", app_exc)  # This will show the custom exception message with traceback
        raise app_exc from e