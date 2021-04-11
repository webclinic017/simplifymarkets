import os
import csv
import json

class File:

    """ Common file operations """

    def __init__(self):
        super().__init__()

    # Read file and return object
    def readFile(self, path, fileName, permission = 'r'):

        fileAbsoluteName = path + '/' + fileName

        with open(fileAbsoluteName, permission) as file:
            reader = csv.reader(file)
            rows = []
            for row in reader:
                rows.append(row)
            file.close()

        return rows

    def writeFile(self, fileName, extension, permission, data):
        
        fileObj = open(fileName + '.' + extension, permission)
        json.dump(data, fileObj)
        fileObj.close()