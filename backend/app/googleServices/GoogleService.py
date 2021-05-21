from django.conf import settings
from google.oauth2 import service_account
from googleapiclient.discovery import build
from . SheetsService import SheetsService
from . DriveService import DriveService

KEY = settings.BASE_DIR + '\\app\\resources\\secretKey.json'

DRIVE = 'drive'

SHEETS = 'sheets'


class GoogleService:
    """ Creates root service and get other gServices object. """

    def __init__(self):
        self.scopes = [
            'https://www.googleapis.com/auth/sqlservice.admin',
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive.file',
            'https://www.googleapis.com/auth/drive'
        ]

        self.credentials = service_account.Credentials.from_service_account_file(
            KEY, scopes=self.scopes)

    def get_drive_service(self):
        """ drive service wrapper. """
        service = build(DRIVE, 'v2', credentials=self.credentials)
        return SheetsService(service)

    def get_sheets_service(self):
        """ sheets service wrapper. """
        service = build(SHEETS, 'v4', credentials=self.credentials)
        return DriveService(service)
