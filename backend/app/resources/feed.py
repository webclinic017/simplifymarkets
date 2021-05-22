from utility.File import File
from django.conf import settings

def get_symbols_info():
    f = File()
    data = f.read(file_name = 'database_index', path =  settings.BASE_DIR + '\\app\\resources\\', extension = 'json')
    return data