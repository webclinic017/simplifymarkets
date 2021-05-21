class DriveService:
    """ class for google drive functions """

    service = None

    def __init__(self, driveService):

        if DriveService.service == None:
            DriveService.service = driveService

    def get_all_files(self, show=True):

        result = []
        pageToken = None

        while True:
            try:
                param = {}
                if pageToken:
                    param['pageToken'] = pageToken
                files = DriveService.service.files().list(**param).execute()
                result.extend(files['items'])
                pageToken = files.get('nextPageToken')
                if not pageToken:
                    break
            except:
                #print('An error occurred: %s' % error)
                break

        if show == True:
            print('Total Files : ' + str(len(result)))

        # for i in range(len(result)):
            # print(result[i]['id'])
        # print('\n\n')

        return result

    def insert_permission(self, fileId, value='', permissionType='anyone', role='writer'):

        newPermission = {
            'value': value,
            'type': permissionType,
            'role': role
        }

        return DriveService.service.permissions().insert(fileId=fileId, body=newPermission).execute()

    def delete_sheet(self, fileId):

        DriveService.service.files().delete(fileId=fileId).execute()
