import sys, json, os

class Common:

    """ Common utilities"""

    def __init__(self):
        super().__init__()

    # Returns size of data/object in KiloBytes
    def sizeOf(self, data, units = 1024, show = True):
        size = sys.getsizeof(data)/units
        if units == 1024:
            suffix = ' KB'

        if show == True:
            print(('%.2f ' + suffix) % size)
        return size

def get_stockdb_index():
    database_index = open(os.getcwd() + '/resources/'+'database_index.json') 
    database_index = json.load(database_index)
    return database_index