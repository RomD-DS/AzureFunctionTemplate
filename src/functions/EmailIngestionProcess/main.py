import logging
import traceback

import time
import azure.functions as func

import yaml
from tqdm import tqdm
import os

from functions.EmailIngestionProcess.lib.ms_graph_process import get_attachments, get_token, get_messages_page, archive_message
from functions.EmailIngestionProcess.lib.pdf_process import get_pages
from functions.EmailIngestionProcess.lib.db_connect import get_mongo_client, upsert_page

def get_config(path="./configconfig.yml"):
    with open(path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    return config

def main(req: func.HttpRequest) -> func.HttpResponse:

    logging.info("Analyze Invoices Process started")
    start = time.time()

    try:
        logging.info("Running invoice analysis...")

        logging.info("Get MailBox configuration...")
        config = get_config()
        mailbox = config["azure"]["mailbox"]
        TENANT_ID = config["azure"]["tenant_id"]
        CLIENT_ID = config["azure"]["client_id"]
        CLIENT_SECRET = config["azure"]["client_secret"]
        folder_mail = config["azure"]["folder_mail"]
        folder_archive = config["azure"]["folder_archive"]

        logging.info("Get DataBase configuration...")
        MONGO_URI = config["mongodb"]["uri"]
        MONGO_DATABASE = config["mongodb"]["database"]
        MONGO_COLLECTION = config["mongodb"]["collection"]

        db_client = get_mongo_client(MONGO_URI)
        
        logging.info("Get Azure Token Access...")
        token = get_token(CLIENT_ID, TENANT_ID, CLIENT_SECRET)


        logging.info("Start Processing Mail...")
        next_page = None
        while True:
            messages, next_page = get_messages_page(mailbox, token, folder_mail, next_page)

            for i, msg in tqdm(enumerate(messages), total=len(messages), desc=f"Batch Processing Email {i}"):
                msg_id = msg["id"]
                email = msg["from"]["emailAddress"]["address"]
                subject = msg["subject"]
                attachments = get_attachments(mailbox, msg_id, token)

                for attachment in attachments:

                    if attachment["contentType"] == "application/pdf" or attachment["name"].lower().endswith(".pdf"):
                        pages_pdf = get_pages(attachment["contentBytes"])
                        filename = attachment["name"].lower().replace(".pdf", "")

                        for j, page_base64 in enumerate(pages_pdf):
                            num_page = 'p_' + str(j + 1)
                            document = {
                                    "msg_id": msg_id,
                                    "email": email,
                                    "subject": subject,
                                    "filename": filename,
                                    "page_number": j + 1,             # num page
                                    "content_base64": page_base64,     # base64 de la page
                                    "status": "save"
                                }

            result = upsert_page(db_client, MONGO_COLLECTION, document)
                            

            archive_message(token, mailbox, msg_id, folder_archive)

        duration = time.time() - start
        logging.info(f"End Processing Mail  {duration:.2f}s")
        return func.HttpResponse("OK")

    except Exception as e:
        duration = time.time() - start
        logging.error("ERROR in Analyze Invoices Process")
        logging.error(f"Message: {str(e)}")
        logging.error("Traceback:")
        logging.error(traceback.format_exc())
        logging.error(f"Process failed after {duration:.2f}s")
        return "ERROR"