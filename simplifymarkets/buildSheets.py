from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account
from googleapiclient.errors import HttpError
from apiclient import errors

# LIST all the FILES
def retrieve_all_files(service):
    result = []
    page_token = None
    while True:
        try:
            param = {}
            if page_token:
               param['pageToken'] = page_token
            files = service.files().list(**param).execute()
            result.extend(files['items'])
            page_token = files.get('nextPageToken')
            if not page_token:
                break
        except errors.HttpError:
            #print('An error occurred: %s' % error)
            break
    
    for i in range(len(result)):
        print(result[i]['id'])
    print('\n\n')
    return result

# Make file PUBLIC
def insert_permission(service, file_id, value = '', permission_type = 'anyone', role = 'writer'):
    new_permission = {
        'value' : value,
        'type' : permission_type,
        'role' : role
    }
    return service.permissions().insert(fileId = file_id, body = new_permission).execute()

# GET
def getSheet(service, spreadsheet_id, ranges = [], include_grid_data = False):
    # Call the Sheets API
    sheet = service.spreadsheets()
    request = sheet.get(spreadsheetId=spreadsheet_id, ranges=ranges, includeGridData=include_grid_data)
    response = request.execute()
    print(response)

# CREATE
def createSheet(service):
    sheet = {
        'properties': {
        'title': "STOCK_DATA"
        }
    }
    spreadSheet = service.spreadsheets().create(body=sheet, fields='spreadsheetId').execute()
    spreadSheetId = str(sheet.get('spreadsheetId'))
    print('Spreadsheet ID: {0}'.format(spreadSheet.get('spreadsheetId')))
    return spreadSheetId
    
# WRITE 
def writeSheet(service, spreadSheetId, symbol = "ITC"):
    values = [
        ['=GOOGLEFINANCE('+symbol+', "ALL", "01/01/1970", TODAY())']
    ]
    body = {
        'values' : values
    }
    range_name = 'Sheet1!A1:A1'
    result = service.spreadsheets().values().update(spreadsheetId=spreadSheetId, range=range_name, valueInputOption='USER_ENTERED', body=body).execute()
    #print('{0} cells updated.'.format(result.get('updatedCells')))


def main():
    SCOPES = ['https://www.googleapis.com/auth/sqlservice.admin', 
          'https://www.googleapis.com/auth/spreadsheets',
          'https://www.googleapis.com/auth/drive.file',
          'https://www.googleapis.com/auth/drive']
    SERVICE_ACCOUNT_FILE = 'sheetkey.json'
    creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    sheetService = build('sheets', 'v4', credentials=creds)
    driveService = build('drive', 'v2', credentials=creds)

    #insert_permission(service = driveService, file_id = '1XucNbcohP3Z_e8kYcL9odGlE1Qx_vFGyCeNYQhLVDgk', permission_type = 'anyone', role = 'reader')
    #changePermission(driveService, '1XucNbcohP3Z_e8kYcL9odGlE1Qx_vFGyCeNYQhLVDgk', )
    #downloadFile(sheetService)
    #spreadSheetId = createSheet(sheetService)
    retrieve_all_files(driveService)
    #delete everything
    # get a list stock symbols - 
    #insert_permission(service = driveService, file_id = '1HBbxqzPvGmv6ml4uxH4ZK6d3ac3n59AecJoQ7oaUZYg', permission_type = 'anyone', role = 'writer')
    #getSheet(sheetService, '1HBbxqzPvGmv6ml4uxH4ZK6d3ac3n59AecJoQ7oaUZYg')
    #writeSheet(service=sheetService, spreadSheetId = '1HBbxqzPvGmv6ml4uxH4ZK6d3ac3n59AecJoQ7oaUZYg')

if __name__ == "__main__":
        main()


"""
def downloadFile(service):
    file_id = '1XucNbcohP3Z_e8kYcL9odGlE1Qx_vFGyCeNYQhLVDgk'
    request = service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download %d%%." % int(status.progress() * 100))
"""