import os
import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from utilities.config_reader import get_config


# ---------------------------------------------------------
# 1️⃣ CREATE GOOGLE DRIVE SERVICE (Supports Shared Drives)
# ---------------------------------------------------------
def get_drive_service():
    json_path = get_config("GoogleDrive", "service_account_json")
    scopes = ["https://www.googleapis.com/auth/drive"]

    creds = service_account.Credentials.from_service_account_file(
        json_path, scopes=scopes
    )
    return build("drive", "v3", credentials=creds)


# ---------------------------------------------------------
# 2️⃣ CREATE DAILY FOLDER INSIDE SHARED DRIVE
# ---------------------------------------------------------
def create_daily_folder(service, parent_id):
    today = datetime.datetime.now().strftime("%Y-%m-%d")

    folder_metadata = {
        "name": today,
        "mimeType": "application/vnd.google-apps.folder",
        "parents": [parent_id],
    }

    folder = service.files().create(
        body=folder_metadata,
        fields="id",
        supportsAllDrives=True
    ).execute()

    return folder["id"]


# ---------------------------------------------------------
# 3️⃣ UPLOAD ANY FILE INTO SHARED DRIVE FOLDER
# ---------------------------------------------------------
def upload_file_to_drive(file_path):
    service = get_drive_service()

    # Shared drive parent folder ID
    parent_id = get_config("GoogleDrive", "folder_id")

    # Optional daily folder creation
    use_daily = get_config("GoogleDrive", "create_daily_folder", fallback="yes")

    if use_daily.lower() == "yes":
        parent_id = create_daily_folder(service, parent_id)

    file_metadata = {
        "name": os.path.basename(file_path),
        "parents": [parent_id],
    }

    media = MediaFileUpload(file_path, resumable=True)

    uploaded = service.files().create(
        body=file_metadata,
        media_body=media,
        fields="id, name",
        supportsAllDrives=True
    ).execute()

    file_id = uploaded["id"]

    # Make publicly viewable
    service.permissions().create(
        fileId=file_id,
        body={"role": "reader", "type": "anyone"},
        supportsAllDrives=True
    ).execute()

    return f"https://drive.google.com/file/d/{file_id}/view?usp=sharing"
