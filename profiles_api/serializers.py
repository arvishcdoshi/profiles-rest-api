from rest_framework import serializers

class HelloSerializer(serializers.Serializer):
    """Serializes a name field for testing our APIView"""
    """We're going to create a simple serializer that accepts a
       name input and then we are going to add this to our API view and
       we'll use it to test the post functionality of our API view"""

    name = serializers.CharField(max_length=10)
       
