import logging
import traceback

import time
import azure.functions as func


def main(mytimer: func.TimerRequest) -> None:

    logging.info("Analyze Invoices Process started")
    start = time.time()

    try:
        logging.info("Running invoice analysis...")

        # Met le code
        mails = get_file_from_email()

        for mail in mails : 

            for files in mail :  


        duration = time.time() - start
        logging.info(f"Analyze Invoices Process finished in {duration:.2f}s")

        return "OK"

    except Exception as e:
        duration = time.time() - start
        logging.error("ERROR in Analyze Invoices Process")
        logging.error(f"Message: {str(e)}")
        logging.error("Traceback:")
        logging.error(traceback.format_exc())
        logging.error(f"Process failed after {duration:.2f}s")
        return "ERROR"