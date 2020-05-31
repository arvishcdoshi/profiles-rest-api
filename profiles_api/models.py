from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.conf import settings

# Create your models here.

class UserProfileManager(BaseUserManager):
    """Manager for user profiles, we specify some functions within the managers that are used to manipulate objects within the model that the manager is for"""

    def create_user(self,email,name,password=None):
        """Create a new user profile"""
        if not email:
            raise ValueError('User must have an email address')

        email=self.normalize_email(email) # It makes the second half of the email address all lowercase..
        user = self.model(email=email, name=name)  #Creation of user model..this creates a new model that the user manager is representing..creates new mmodel object

        user.set_password(password) # Ensures that password is stored as hash in the database..and not as a normal string
        user.save(using=self._db)

        return user

    def create_superuser(self,email,name,password):
        """Create and save a new superuser with given details"""
        user = self.create_user(email,name,password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user

class UserProfile(AbstractBaseUser,PermissionsMixin):
    """ Database model for the users in the system """
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default = False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        """Retrieve full name of user"""
        return self.name

    def get_short_name(self):
        """Retrieve short name of user"""
        return self.name

    def __str__(self):
        """Return string representation of our user"""
        return self.email



"""Below model is the model we are gonna use to allow users to store status updates in the system..
Everytime they create a new update,its gonna create a new ProfileFeedItem object and associate
that object with the user that created it..The way you link models to other models in Django is
using a foreign key...when u use a foreign key field, it sets up a foreign key relationship in
the database to a remote model..benefit of doing this is that it allows you to ensure that the
integrity of the database is maintained...so you can never create ProfileFeedItem for a
user profile that doesn't exist
"""



class ProfileFeedItem(models.Model):
    user_profile = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    status_text = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return the models as a string, below line means when we convert model to a string,we want to see the status text value associated to the model"""
        return self.status_text
