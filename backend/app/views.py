from . serializers import employeesSerializer
from . models import employee
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response

def index(request):
    return HttpResponse("Awesome!")

"""
from .coinbase.Login import *
def execute():
    # blob = json.dumps(blob, indent=4, sort_keys=True)
    api_url = 'https://api.coinbase.com/v2/'
    auth = ExchangeAuth(COINBASE_API_KEY, COINBASE_API_SECRET)
    r = requests.get(api_url + 'user', auth=auth)
    return r.json()
"""

class employeeList(APIView):

    def get(self, request):
        employees1 = employee.objects.all()
        result = employeesSerializer(employees1, many = True)
        return Response(result.data)

    def post(self):
        return 