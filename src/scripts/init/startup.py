from simplifymarkets.simplifymarkets.googleServices import GoogleService

googleService = GoogleService()
googleService.create_drive_service().get_all_files()