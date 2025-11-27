import logging
import azure.functions as func
import time

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("HTTP trigger function started")
    
    start = time.time()

    try:
        logging.info("HELLO WORLD 👋")
        duration = time.time() - start

        return func.HttpResponse(
            f"HELLO WORLD 👋 (finished in {duration:.2f}s)",
            status_code=200
        )

    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return func.HttpResponse("ERROR", status_code=500)
