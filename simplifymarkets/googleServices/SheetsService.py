class SheetsService:

    """ class for google sheets functions """

    service = None

    # Constructor
    def __init__(self, sheetService):
        if SheetsService.service == None:
            SheetsService.service = sheetService

    # Get the sheet
    def get_sheet(self, spreadsheetId, ranges = [], include_grid_data = False, show = True):

        request = SheetsService.service.spreadsheets().get(spreadsheetId=spreadsheetId, ranges = ranges, includeGridData = include_grid_data)
        response = request.execute()
        if show == True:
            print(response)
        return response


    # CREATE
    def create_sheet(self, show = True):

        sheet = {
            'properties': {
            'title': "Default_Title"
            }
        }

        request = SheetsService.service.spreadsheets().create(body=sheet, fields='spreadsheetId')
        response = request.execute()

        if show == True:
            print('Spreadsheet ID: {0}'.format(response.get('spreadsheetId')))

        return response


    # WRITE
    def write_sheet(self, spreadSheetId, symbol):
        values = [
            ['=GOOGLEFINANCE("'+symbol+'", "ALL", "01/01/1970", TODAY())']
        ]
        body = {
            'values' : values
        }
        range_name = 'Sheet1!A1:A1'

        request = SheetsService.service.spreadsheets().values().update(spreadsheetId=spreadSheetId, range=range_name, valueInputOption='USER_ENTERED', body=body)
        response = request.execute()

        print('writeSheet {0} cells updated.'.format(response.get('updatedCells')))