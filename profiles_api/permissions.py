from rest_framework import permissions


class UpdateOwnProfile(permissions.BasePermission):

    """Allow the users to edit their own profile"""

    def has_object_permission(self,request,view,obj):
        """Check user is trying to edit their own profile"""

        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.id == request.user.id



# line no 13:- if the request made by the user is not in safe methods, for example they try to execute HTTP PUT,
# we're gonna check the object they are updating matches their authenticated user profile  that is added to the
#authentication of the request
"""When you authenticate a request in the django-restframework, it will assign the authenticated user profile to the request and we can
use this to compare it to the object that is being updated and make sure they have the same ID...line no 13 returns true if user is trying
to update his/her own profile...if not so it returns false  SAFE_METHODS are GET AND POST"""



class UpdateOwnStatus(permissions.BasePermission):
    """Allow users to update their own status"""

    def has_object_permission(self,request,view,obj):
        """Check if the user is updating its own status"""

        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user_profile.id == request.user.id
