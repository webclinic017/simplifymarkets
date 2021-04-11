class DriveService:

    """ class for google drive functions """

    driveService = None

    # Class Constructor
    def __init__(self, driveService):

        if driveService == None:
            DriveService.driveService = driveService

    # Returns list of all files
    def getAllFiles(self):

        result = []
        pageToken = None

        while True:
            try:
                param = {}
                if pageToken:
                    param['pageToken'] = pageToken
                files = driveService.files().list(**param).execute()
                result.extend(files['items'])
                pageToken = files.get('nextPageToken')
                if not pageToken:
                    break
            except:
                #print('An error occurred: %s' % error)
                break

        return result

    # Make file PUBLIC
    def insertPermission(self, fileId, value = '', permissionType = 'anyone', role = 'writer'):
        
        newPermission = {
            'value' : value,
            'type' : permissionType,
            'role' : role
        }

        return driveService.permissions().insert(fileId = fileId, body = newPermission).execute()

    # Delete a file
    def deleteSheet(self, fileId):

        driveService.files().delete(fileId=fileId).execute()