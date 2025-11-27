from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, PyMongoError
import os

def get_mongo_client(MONGO_URI):
    """
    Retourne un client MongoDB unique et valide.
    Lève une exception si la connexion échoue.
    """
    try:
        client = MongoClient(MONGO_URI)
        client.admin.command("ping")

        return client
    except ConnectionFailure:
        raise Exception("Failed to connect to MongoDB server.")

def upsert_page(db, collection_name, document):
    """
    Met à jour la page si elle existe déjà,
    sinon insère la page (UPSERT).
    """

    collection = db[collection_name]

    # Les champs qui définissent de façon unique une page d’un PDF
    filter_query = {
        "msg_id": document["msg_id"],
        "email": document["email"],
        "subject": document["subject"],
        "filename": document["filename"],
        "page_number": document["page_number"]
    }

    # Les champs à mettre à jour ou créer
    update_query = {
        "$set": {
            "content_base64": document["content_base64"],
            "status": document["status"]
        }
    }

    # upsert=True = update si existe, insert sinon
    result = collection.update_one(filter_query, update_query, upsert=True)
    return result