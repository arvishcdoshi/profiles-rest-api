from rest_framework.views import APIView
from rest_framework.response import Response


class HelloApiView(APIView):
    """Test API view"""
    def get(self,request,format=None):
        """Returns a list of APIView features..request object contains details about the request made to API"""

        an_apiview = [
        'Uses HTTP methods as function (get,post,patch,put,delete)',
        'Is similar to a traditional Django View',
        'gives you the most control over your application logic',
        'is mapped manually to URLs',
        ]
        return Response({'message':'Hello','an_apiview':an_apiview})  # Response object is converted to JSON...in order to be JSON, it needs to be converted to a list or dictionary
