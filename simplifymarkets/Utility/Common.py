import sys

class Common:

    """ Common utilities"""

    def __init__(self):
        super().__init__()

    # Returns size of data/object in KiloBytes
    def sizeOf(self, data, units = 1024, print = True):
        size = sys.getsizeof(data)/units
        if print == True:
            print(size)
        return size

