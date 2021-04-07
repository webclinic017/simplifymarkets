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
    spreadSheetId = str(spreadSheet.get('spreadsheetId'))
    print('Spreadsheet ID: {0}'.format(spreadSheetId))
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

def stockSymbols(selector):
    SYMBOLS_PATH_excel = "symbols"
    xlsx_file = Path(SYMBOLS_PATH_excel, selector)
    print(xlsx_file)
    wb_obj = openpyxl.load_workbook(xlsx_file)
    # Read the active sheet:
    sheet = wb_obj.active
    symbols = sheet.max_row
    print(symbols)
    stock_symbols = []
    for i in range(2, symbols + 1):
        raw_symbol = "A" + str(i)
        raw_data = sheet[raw_symbol].value
        raw_data = raw_data.split(", ")[1]
        raw_data = raw_data.split('"')[1]
        raw_data = raw_data.split('_')[1]
        raw_data = raw_data.split('-')[0]
        stock_symbols.insert(i, raw_data)
    return stock_symbols

def json_writer(thisdict, index):
    filename = index + ".json"
    a_file = open(filename, "w")
    json.dump(thisdict, a_file)
    a_file.close()

    a_file = open(filename, "r")
    output = a_file.read()
    print(output)
    a_file.close()

def listIndex(selectIndex):
    index = ["BSEAuto MW.xlsx","BSEFMC MW.xlsx", "BSEIT MW.xlsx", "BSEMetal MW.xlsx", "BSEOnG MW.xlsx", "BSEPower MW.xlsx","BSERealty MW.xlsx", "Nifty50 MW.xlsx","NiftyAuto MW.xlsx","NiftyBank MW.xlsx","NiftyCommodities MW.xlsx", "NiftyConsumption MW.xlsx", "NiftyEnergy MW.xlsx","NiftyFMCG MW.xlsx","NiftyInfra MW.xlsx", "NiftyIT MW.xlsx","NiftyMedia MW.xlsx","NiftyMetal MW.xlsx","NiftyMidCap50 MW.xlsx","NiftyMNC MW.xlsx","NiftyNext50 MW.xlsx","NiftyPharma MW.xlsx","NiftyPSE MW.xlsx","NiftyPSUBank MW.xlsx","NiftyRealty MW.xlsx","NiftyServSector MW.xlsx"]
    return index[selectIndex]

def symbolsSheet(sheetService, stock_symbols, indexname):
    thisdict = {}
    for i in range(len(stock_symbols)):
        spreadSheetId = createSheet(sheetService)
        time.sleep(4)
        thisdict[stock_symbols[i]] = spreadSheetId
        json_writer(thisdict,indexname)
    return thisdict

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
    # dictonary or hash table key = symbol and value = sheel id
    #link to excel to reterive symbols C:\Zerodha\Pi\LinkExcel

    selector = 3
    indexname = str(listIndex(selector))
    print(indexname)
    stock_symbols = stockSymbols(indexname)
    symbolsSheet(sheetService, stock_symbols, indexname)


    #retrieve_all_files(driveService)
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