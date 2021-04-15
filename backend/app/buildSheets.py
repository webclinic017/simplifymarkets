from googleServices.GoogleService import GoogleService
from googleServices.DriveService import DriveService
from googleServices.SheetsService import SheetsService
import googleServices
import time
from utility.Common import * 
from utility.File import *


"""
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

    index[symbolsList[i]] = spreadSheetId 
    writeIndex(index)
"""

def main():

    commonUtil = Common()
    fileUtil = File()

    googleService = GoogleService('utility/', 'secretKey.json')
    driveService = DriveService(googleService.get_drive_service())
    sheetsService = SheetsService(googleService.get_sheets_service())

    reader = fileUtil.read_file(os.getcwd() + '/resources/', 'symbols.csv')
    print(len(reader))
    #print(len(driveService.get_all_files()))
    #commonUtil.sizeOf(reader)

    for i in range(270):
        sheetsService.create_sheet()
        time.sleep(8)

if __name__ == "__main__":
        main()
