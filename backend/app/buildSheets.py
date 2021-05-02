from googleServices.GoogleService import GoogleService
from googleServices.DriveService import DriveService
from googleServices.SheetsService import SheetsService
from googleapiclient.http import MediaIoBaseDownload
import googleServices
import time
from utility.Common import * 
from utility.File import *
import json
import io

commonUtil = Common()
fileUtil = File()
googleService = GoogleService('utility/', 'secretKey.json')
driveService = DriveService(googleService.get_drive_service())
sheetsService = SheetsService(googleService.get_sheets_service())

def find_CAGR(first_price, curr_price, total_days):
    if total_days < 252:
        return -1
    
    years = total_days / 252.0
    CAGR = ((curr_price / first_price)**(1/float(years)) - 1) * 100
    return CAGR


def build_sheets():
    
    with open(os.getcwd() + '/resources/'+'database_index.json') as json_file:
        database_index = json.load(json_file)
    

    try:
        flag = False
        failed_symbol = 'UJJIVANSFB'

        for symbol in database_index:
            if symbol == failed_symbol:
                flag = True
            
            if flag == True:
                sheetsService.write_sheet(database_index[symbol], symbol)
                print('write success : ' + symbol)
                time.sleep(8)
    except:
        print('broke at :' + symbol)
        failed_symbol = symbol


def analysis():
    database_index = open(os.getcwd() + '/resources/'+'database_index.json') 
    database_index = json.load(database_index)

    #print(sheetsService.get_sheet(database_index['DRREDDY']))
    #driveService.insert_permission(database_index['DRREDDY'])
    print(len(sheetsService.read_sheet(database_index['TCS'])))

    print(commonUtil.sizeOf(sheetsService.read_sheet(database_index['TCS'])))

    return
    CLOSE = 4
    flag = False
    stop_symbol = 'ZEELEARN'

    try:
        for symbol in database_index:
            if symbol == stop_symbol:
                flag = True
            
            if flag == True:
                stock_data = sheetsService.read_sheet(database_index[symbol])
                #print(stock_data)
                total_days = len(stock_data)-1
                curr_price = float(stock_data[total_days][CLOSE])
                first_price = float(stock_data[1][CLOSE])
                cagr = find_CAGR(first_price, curr_price, total_days)
                years = total_days/252.0

                if cagr >  5:
                    print(symbol + " : "  + str(find_CAGR(first_price, curr_price, total_days)) + " % , " + str(total_days/252.0) + ' years')
                    time.sleep(3)
                else:
                    time.sleep(8)
    except:
        print('Break at : ' + symbol)
            

def main():
    #print(find_CAGR(100, 133, 3*252))
    analysis()
    

if __name__ == "__main__":
    main()


"""
            write = symbol + " : "  + str(find_CAGR(first_price, curr_price, total_days)) + " % , " + str(total_days/252.0) + ' years'
            filter_symbol[symbol] = write
            fileUtil.write_file(filter_symbol, os.getcwd() + '/resources/', 'filter_symbols', 'json')
            

            if cagr < 5:
                filter_symbol.append(symbol)
                fileUtil.write_file(filter_symbol, os.getcwd() + '/resources/', 'filter_symbols', 'json')
                time.sleep(8)
                continue
ORCHPHARMA
reader = fileUtil.read_file(os.getcwd() + '/resources/', 'symbols_nse.csv')
#print(len(reader))

all_files = driveService.get_all_files()
spread_sheetids = []
for i in range(len(all_files)):
    spread_sheetids.append(all_files[i]['id'])
    #print(spread_sheetids[i])

i = 0
database_index = {}
for row in reader:
    symbol = row[0]
    spread_sheetid = spread_sheetids[i]
    print(symbol)
    print(spread_sheetid)
    database_index[symbol] = spread_sheetid
    i = i + 1

fileUtil.write_file(database_index, os.getcwd() + '/resources/', 'database_index', 'json')

#print(len(allfiles))
for i in range(184):
    sheetsService.create_sheet()
    time.sleep(8)

#print(len(driveService.get_all_files()))
#commonUtil.sizeOf(reader)
"""


