from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account
from googleapiclient.errors import HttpError
from apiclient import errors
import openpyxl
from pathlib import Path
import time
import json
import re
import csv
import sys

# LIST all the FILES
def getAllSheets(driveService):
    result = []
    page_token = None
    while True:
        try:
            param = {}
            if page_token:
               param['pageToken'] = page_token
            files = driveService.files().list(**param).execute()
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
    request = service.spreadsheets().get(spreadsheetId=spreadsheet_id, ranges=ranges, includeGridData=include_grid_data)
    response = request.execute()
    print(response)

# CREATE
def createSheet(sheetService):
    sheet = {
        'properties': {
        'title': "STOCK_DATA"
        }
    }
    spreadSheet = sheetService.spreadsheets().create(body=sheet, fields='spreadsheetId').execute()
    spreadSheetId = str(spreadSheet.get('spreadsheetId'))
    print('Spreadsheet ID: {0}'.format(spreadSheetId))
    return spreadSheetId

# WRITE 
def writeSheet(service, spreadSheetId, symbol):
    values = [
        ['=GOOGLEFINANCE("'+symbol+'", "ALL", "01/01/1970", TODAY())']
    ]
    body = {
        'values' : values
    }
    range_name = 'Sheet1!A1:A1'
    result = service.spreadsheets().values().update(spreadsheetId=spreadSheetId, range=range_name, valueInputOption='USER_ENTERED', body=body).execute()
    print('writeSheet {0} cells updated.'.format(result.get('updatedCells')))

# DELETE
def deleteSheet(service, spreadSheetId):
    service.files().delete(fileId=spreadSheetId).execute()

# LIST all SYMBOLS - NSE
def getSymbols():
    #print(os.curdir)
    SYMBOLS_PATH = os.getcwd() + '/resources/symbols.csv'
    symbolsList = []
    with open(SYMBOLS_PATH, 'r') as file:
        reader = csv.reader(file)
        rowCount = 0
        for row in reader:
            if rowCount == 0:
                rowCount += 1
                continue
            symbolsList.append(row[0])
    #print(sys.getsizeof(symbolsList)/(1024))
    return symbolsList

# WRITE the Index to file
def writeIndex(index):
    filename = 'index.json'
    fileObj = open(filename, "w")
    json.dump(index, fileObj)
    fileObj.close()

# CREATE the SHEET with FORMULA for every SYMBOL and write the index(symbol, spreadSheetId)
def bootstrapStocksData(sheetService):
    symbolsList = getSymbols()
    index = {}

    for i in range(len(symbolsList)):
        spreadSheetId = createSheet(sheetService)
        time.sleep(1)
        writeSheet(sheetService, spreadSheetId, symbolsList[i])
        index[symbolsList[i]] = spreadSheetId

    writeIndex(index)

# DELETE ALL the Sheets
def resetStockData(driveService):
    allSheets = getAllSheets(driveService)
    for i in range(len(allSheets)):
        deleteSheet(driveService, allSheets[i]['id'])

def main():
    SCOPES = [
          'https://www.googleapis.com/auth/sqlservice.admin',
          'https://www.googleapis.com/auth/spreadsheets',
          'https://www.googleapis.com/auth/drive.file',
          'https://www.googleapis.com/auth/drive'
    ]
    SERVICE_ACCOUNT_FILE = 'sheetkey.json'
    creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    sheetService = build('sheets', 'v4', credentials=creds)
    driveService = build('drive', 'v2', credentials=creds)

    resetStockData(driveService)

    #bootstrapStocksData(sheetService)
    #insert_permission(driveService, '1nCwDnGWuH7kyq5H5Un8v3LKzb7ntFDvMGMLCyxTtPGQ')
    #getSheet(sheetService, '1nCwDnGWuH7kyq5H5Un8v3LKzb7ntFDvMGMLCyxTtPGQ')

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