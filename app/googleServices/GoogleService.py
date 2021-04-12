from google.oauth2 import service_account
from googleapiclient.discovery import build

class GoogleService:

    """ Core class to connect to google infrastructure and generate service objects. """

    DRIVE = 'drive'
    SHEETS = 'sheets'

    # Constructor
    def __init__(self, path, keyFileName):

        self.scopes = [
          'https://www.googleapis.com/auth/sqlservice.admin',
          'https://www.googleapis.com/auth/spreadsheets',
          'https://www.googleapis.com/auth/drive.file',
          'https://www.googleapis.com/auth/drive'
        ]

        self.path = path
        self.keyFileName = keyFileName
        self.credentials = service_account.Credentials.from_service_account_file(path + keyFileName, scopes = self.scopes)

    # Get Service object
    def _get_service(self, serviceName, version):
        return build(serviceName, version, credentials = self.credentials)

    # Get DriveService
    def get_drive_service(self):
        return self._get_service(self.DRIVE, 'v2')

    # Get SheetService
    def get_sheets_service(self):
        return self._get_service(self.SHEETS, 'v4')