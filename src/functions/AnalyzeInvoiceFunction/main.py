import logging
import traceback

import time
import azure.functions as func


def main() -> None:

    logging.info("Analyze Invoices Process started")
    start = time.time()

    try:
        logging.info("Running invoice analysis...")

        # Met le code
        page = get_page()
        #### Function LLM Process

        result = llm_process()

        ### Save In MongoDB 
        save_mongodb(result)


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