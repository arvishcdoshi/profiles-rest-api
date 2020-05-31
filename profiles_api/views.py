from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status  # list of handy HTTP status codes when returning response from API
from rest_framework import viewsets

from rest_framework import filters
from rest_framework.authtoken.views import ObtainAuthToken # a view that comes with Django-rest-framework that we can use to generate an Auth-Token
from rest_framework.settings import api_settings
#from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from profiles_api import serializers #created in serializers.py
from profiles_api import permissions
from profiles_api import models

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



class HelloViewSet(viewsets.ViewSet):
    """Test API ViewSet"""

    serializer_class = serializers.HelloSerializer

    def list(self,request):
        """Return a Hello Message"""

        a_viewset = [
        'Uses actions (list,create, retrieve, update, partial_update)',
        'Automatically maps to URLs using Routers',
        'Provides more functionality with less code'
        ]

        return Response({'message':'Hello','a_viewset':a_viewset})


    def create(self,request):
        """Create a new hello message"""
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}!'
            return Response({'message':message})

        else:
            return Response(
               serializer.errors,
               status = status.HTTP_400_BAD_REQUEST
            )


    def retrieve(self,request,pk=None):
        """Handle getting object by getting its ID"""
        return Response({'http_method':'GET'})

    def update(self,request,pk=None):
        """Handle updating an object"""
        return Response({'http_method':'PUT'})

    def partial_update(self,request,pk=None):
        """Handle updating part of object, partial_update maps to HTTP 'PATCH' request"""
        return Response({'http_method':'PATCH'})

    def destroy(self,request,pk=None):
        """Handle removing an object"""
        return Response({'http_method':'DELETE'})




class UserProfileViewset(viewsets.ModelViewSet):

    """Handle Creating and Updating Profiles"""

    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name','email',)


class UserLoginApiView(ObtainAuthToken):

    """Handle creating user Authentication tokens"""
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES # enables functionality in Django-Admin



class UserProfileFeedViewSet(viewsets.ModelViewSet):
    """Handles creating, reading and updating profile feed items"""
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.ProfileFeedItemSerializer
    queryset = models.ProfileFeedItem.objects.all() # we're gonna manage all of our profile feed item objects from our model in our  viewset
    permission_classes = (
       permissions.UpdateOwnStatus,
       #IsAuthenticatedOrReadOnly
       IsAuthenticated
    )


    def perform_create(self,serializer): # used for customizing the logic for creating an object, we can do this by using the perform_create function..this perform_create function gets called everytime we perform HTTP POST to our viewset..
        """Sets the user profile to the logged in user"""
        serializer.save(user_profile=self.request.user)




    """ Explanation of line no 137...
When a new object is created, djangorestframework calls perform_create and it passes in the serializer that we're using to create
object ...serializer is a model serializer...so it has a save function assigned to it and that save function is used to save the
contents of the serializer to an object in the database..we're calling serializer.save() and we're passing an additional keyword
for the user profile...This gets passed in addition to all of the items in the serializer that have been validated

We've set user_profile to self.request.user..the request object is an object that gets passed into all viewsets every time a request is made
and as the name suggests, it contains all of the details about the request being made to the view set..because we've added TokenAuthentication
to our viewset, if the user has authenticated, then the request will have a user associated to the authenticated user and so this
user fiels gets added whenever the user is authenticated and if they're not authenticated, then it's just set to an anonymous user account
    """
