from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os

g_login = GoogleAuth()
drive = GoogleDrive(g_login)

file_path = 'OPERATOR_WELLBORE.csv'

with open(file_path, "r") as file:
    file_drive = drive.CreateFile({'title': os.path.basename(file.name),
                                  "parents":  [{"id": 'TEXASSCRAPE'}],
                                  "mimeType": "application/vnd.google-apps.folder"
    })
    file_drive.SetContentString(file.read())
    file_drive.Upload()