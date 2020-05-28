from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status  # list of handy HTTP status codes when returning response from API

from profiles_api import serializers #created in serializers.py


class HelloApiView(APIView):
    """Test API view"""
    serializer_class = serializers.HelloSerializer # This configures our APIView to have the serializer class
    def get(self,request,format=None):
        """Returns a list of APIView features..request object contains details about the request made to API"""

        an_apiview = [
        'Uses HTTP methods as function (get,post,patch,put,delete)',
        'Is similar to a traditional Django View',
        'gives you the most control over your application logic',
        'is mapped manually to URLs',
        ]
        return Response({'message':'Hello','an_apiview':an_apiview})  # Response object is converted to JSON...in order to be JSON, it needs to be converted to a list or dictionary

    def post(self,request):
       """Create a hello message with our name"""
       serializer = self.serializer_class(data=request.data) # Retrieve the serializer and pass in the data that was sent in request

# request.data(data passed in url) is assigned to serializer class and this is assigned to variable called serializer...
       if serializer.is_valid():
           name = serializer.validated_data.get('name') # Retrieving the 'name' field from validated data..
           message = f'Hello {name}'
           return Response({'message':message})

       else:
           return Response(
           serializer.errors,
           status = status.HTTP_400_BAD_REQUEST
           )

    def put(self,request,pk=None):
        return Response({'method':'PUT'})


    def patch(self,request,pk=None):
        """Handle a partial update of an object"""
        return Response({'method':'PATCH'})

    def delete(self,request,pk=None):
        """Delete an object"""
        return Response({'method':'DELETE'})
