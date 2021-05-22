import requests, time, hmac, hashlib
from requests.auth import AuthBase

COINBASE_API_KEY = 'lqWSwZ85ldfoxV4p'
COINBASE_API_SECRET = ''

""" Class to do user authentication """

class ExchangeAuth():
    def __init__(self, api_key, secret_key):
        self.api_key = api_key
        self.secret_key = secret_key

    """ call operator implementation """
    def __call__(self, request):
        timestamp = str(int(time.time()))
        message = timestamp + request.method.upper() + request.path_url + (request.body or '')
        message = message.encode()
        signature = hmac.new(self.secret_key.encode(), message, hashlib.sha256).hexdigest()

        request.headers.update({
            'CB-ACCESS-SIGN' :  signature,
            'CB-ACCESS-TIMESTAMP' : timestamp,
            'CB-ACCESS-KEY' :  self.api_key,
        })

        return request

api_url = 'https://api.coinbase.com/v2/prices/BTC-USD/buy'
auth = ExchangeAuth(COINBASE_API_KEY, COINBASE_API_SECRET)

# Get current user
r = requests.get(api_url, auth=auth)
print(r.json())

"""
from .coinbase.Login import *
def execute():
    # blob = json.dumps(blob, indent=4, sort_keys=True)
    api_url = 'https://api.coinbase.com/v2/'
    auth = ExchangeAuth(COINBASE_API_KEY, COINBASE_API_SECRET)
    r = requests.get(api_url + 'user', auth=auth)
    return r.json()
"""