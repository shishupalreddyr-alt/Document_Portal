## Log the information of the execution flow events enabling the 
# tracing of the application's behavior and identifying potential issues.
#Custom log file could be  .txt file or pdf or .doc file.
##this can also be on consloe, for ex Python gives logging module 
# used in production ## 1. structlog, logGuru, logging   ---- used to create LOG file

import sys
import traceback  ## capture detailed execution 
from logger.custom_logger import CustomLogger


class DocumentPortalException(Exception):
    """Custom exception for Document Portal"""
    def __init__(self,error_message:str,error_details:sys):
        print(error_details.exc_info())
        _,_,exc_tb=error_details.exc_info()
        #Filename
        self.file_name=exc_tb.tb_frame.f_code.co_filename
        #Line number 
        self.lineno=exc_tb.tb_lineno
        #Error message 
        self.error_message=str(error_message)
        #Error details formated 
        self.traceback_str = ''.join(traceback.format_exception(*error_details.exc_info())) 
    def __str__(self):
       return f"""
        Error in [{self.file_name}] at line [{self.lineno}]
        Message: {self.error_message}
        Traceback:
        {self.traceback_str}
        """
logger=CustomLogger().get_logger("__file__")
    
if __name__ == "__main__":
    try:
    # Simulate an error
        a = 1 / 0
        print(a)
    except Exception as e:
        app_exc=DocumentPortalException(e,sys) 
        logger.error(app_exc)
        #logger.error("An error occurred in the Document Portal application.")
        #raise app_exc
