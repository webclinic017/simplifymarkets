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

from googleServices.GoogleService import GoogleService
from googleServices.DriveService import DriveService
from utility.Common import * 
from utility.File import *

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
def deleteSheet(driveService, spreadSheetId):
    driveService.files().delete(fileId=spreadSheetId).execute()

# LIST all SYMBOLS - NSE
def getSymbols():
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

    try:
        for i in range(len(symbolsList)):
            time.sleep(8)
            print(str(i+1)+' ', end="")
            spreadSheetId = createSheet(sheetService)
            #writeSheet(sheetService, spreadSheetId, symbolsList[i])
    except:
        #writeIndex(index)
        print('Index Created till : '+i)

    """
    index[symbolsList[i]] = spreadSheetId 
    writeIndex(index)
    """

# DELETE ALL the Sheets
def resetStockData(driveService):
    allSheets = getAllSheets(driveService)
    for i in range(len(allSheets)):
        print('Deleting : '+allSheets[i]['id'])
        deleteSheet(driveService, allSheets[i]['id'])
    print('\n\n')


def main():
    commonUtil = Common()
    fileUtil = File()
    googleService = GoogleService('utility/', 'secretKey.json')
    driveService = DriveService(googleService.getDriveService())

    reader = fileUtil.readFile(os.getcwd() + '/resources/', 'symbols.csv')
    commonUtil.sizeOf(reader)

if __name__ == "__main__":
        main()
