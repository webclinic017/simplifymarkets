import os
import csv
import json

""" Common file operations """

class File:

    """ Read file and return object. """
    def read(self, file_name, extension, path = None, permission = 'r'):
        assert (file_name != '')
        assert (extension != '')

        if path[-1] != '/':
            path += '/'

        absolute_file_name = path + file_name + '.' + extension
        file = None

        try:
            file = open(absolute_file_name, permission)
            file_data = None
            if extension == 'csv':
                reader = csv.reader(file)
                file_data = []
                for row in reader:
                    file_data.append(row)
            elif extension == 'json':
                file_data = json.load(file)
        except Exception as e:
            print(e)
        
        if file != None:
            file.close()

        return file_data

    # Write file
    def write_file(self, data, path, fileName, extension, permission = 'w'):
        
        fileObj = open(path + fileName + '.' + extension, permission)
        json.dump(data, fileObj)
        fileObj.close()