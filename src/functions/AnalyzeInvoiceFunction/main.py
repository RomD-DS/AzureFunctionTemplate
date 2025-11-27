import logging
import time
import azure.functions as func

def main(mytimer: func.TimerRequest) -> None:
    logging.info("Hello World Function started")
    start = time.time()

    try:
        logging.info("Doing Hello World work...")

        # Hello World
        logging.info("HELLO WORLD 👋")

        duration = time.time() - start
        logging.info(f"Hello World finished in {duration:.2f}s")

    except Exception as e:
        duration = time.time() - start
        logging.error("ERROR in Hello World")
        logging.error(f"Message: {str(e)}")
        logging.exception("Traceback:")
        logging.error(f"Process failed after {duration:.2f}s")