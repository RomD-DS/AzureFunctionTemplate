import msal
import requests
import base64

def get_token(CLIENT_ID, TENANT_ID, CLIENT_SECRET):
    app = msal.ConfidentialClientApplication(
        client_id=CLIENT_ID,
        authority=f"https://login.microsoftonline.com/{TENANT_ID}",
        client_credential=CLIENT_SECRET
    )
    result = app.acquire_token_for_client(
        scopes=["https://graph.microsoft.com/.default"]
    )
    return result["access_token"]

def get_messages_page(mailbox, token, folder_mail, next_url=None):
    headers = {"Authorization": f"Bearer {token}"}

    if next_url:
        url = next_url
    else:
        url = f"https://graph.microsoft.com/v1.0/users/{mailbox}/mailFolders/{folder_mail}/messages?$top=20"

    res = requests.get(url, headers=headers).json()

    messages = res.get("value", [])
    next_page = res.get("@odata.nextLink", None)

    return messages, next_page

def get_attachments(mailbox, message_id, token):
    headers = {"Authorization": f"Bearer {token}"}
    url = f"https://graph.microsoft.com/v1.0/users/{mailbox}/messages/{message_id}/attachments"

    res = requests.get(url, headers=headers).json()
    files = []

    for att in res.get("value", []):
        if att["@odata.type"] == "#microsoft.graph.fileAttachment":
            filename = att["name"]
            content = base64.b64decode(att["contentBytes"])
            with open(filename, "wb") as f:
                f.write(content)
            files.append(filename)

    return files

def archive_message(token, mailbox, message_id, folder_archive):
    headers = {"Authorization": f"Bearer {token}"}
    url = f"https://graph.microsoft.com/v1.0/users/{mailbox}/messages/{message_id}/move"

    data = {"destinationId": folder_archive}
    res = requests.post(url, headers=headers, json=data)

    return res.status_code == 201 or res.status_code == 200