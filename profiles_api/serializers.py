from rest_framework import serializers

from profiles_api import models


class HelloSerializer(serializers.Serializer):
    """Serializes a name field for testing our APIView"""
    """We're going to create a simple serializer that accepts a
       name input and then we are going to add this to our API view and
       we'll use it to test the post functionality of our API view"""

    name = serializers.CharField(max_length=10)



class UserProfileSerializer(serializers.ModelSerializer):
    """Serializes a user profile object"""


#meta class is used to configure serializer to point to a specific model in our project
    class Meta:
        model = models.UserProfile
        fields = ('id','email','name','password') #list of fields in our model that we wish to manage through serializer
        extra_kwargs = {
        'password':{
            'write_only':True,
            'style': {'input_type':'password'} # ensure dots(..) display when inputing passwords..
        }
    }

    def create(self,validated_data):
        """Create and return new user"""
        user = models.UserProfile.objects.create_user(        # creating and returning new user from User profile model manager
        email = validated_data['email'],
        name = validated_data['name'],
        password = validated_data['password']
        )
        return user


    def update(self,instance,validated_data):
        """Handle updating user account"""
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)

        return super().update(instance,validated_data)



class ProfileFeedItemSerializer(serializers.ModelSerializer):
    """Serializes profile feed items"""

    class Meta:
        model = models.ProfileFeedItem # sets our serializer to ProfileFeedItem model created in models.py
        fields = ('id','user_profile','status_text','created_on') #
        extra_kwargs = {
        'user_profile':{'read_only':True}
        }
