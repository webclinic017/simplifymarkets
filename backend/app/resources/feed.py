from utility.File import File
import os

def get_symbols_info():
    f = File()
    data = f.read(file_name = 'database_index', path =  os.getcwd() + '\\app\\resources\\', extension = 'json')
    return data