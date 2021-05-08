from django.http import HttpResponse
from django.shortcuts import render
from .coinbase.Login import *
import json

def index(request):
    blob = execute()
    blob = json.dumps(blob, indent=4, sort_keys=True)
    return HttpResponse(str(blob))
    


def execute():
    api_url = 'https://api.coinbase.com/v2/'
    auth = ExchangeAuth(COINBASE_API_KEY, COINBASE_API_SECRET)
    r = requests.get(api_url + 'user', auth=auth)
    return r.json()
