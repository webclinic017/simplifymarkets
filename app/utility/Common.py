import sys

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

