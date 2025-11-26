import logging
import traceback
import time
import azure.functions as func

from lib.business_rules_process import *



def main(mytimer: func.TimerRequest) -> None:

    logging.info("Business Rules Process started")
    start = time.time()

    try:
        logging.info("Running Business Rules...")
        duration = time.time() - start

        ###Code
        folders = get_files_from_sharepoint()
        business_rules_process()



        logging.info(f"Mail Ingestion Process finished in {duration:.2f}s")

        return "OK"

    except Exception as e:
        duration = time.time() - start

        logging.error("ERROR in Business Rules Process")
        logging.error(f"Message: {str(e)}")
        logging.error("Traceback:")
        logging.error(traceback.format_exc())
        logging.error(f"Process failed after {duration:.2f}s")

        return "ERROR"
