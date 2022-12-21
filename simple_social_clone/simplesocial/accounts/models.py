from django.db import models
from django.contrib import auth # built-in authentication utilities from Django

# Create your models here.
# REFER: https://docs.djangoproject.com/en/4.1/topics/auth/customizing/#custom-users-and-permissions
class User(auth.models.User, auth.models.PermissionsMixin): # Custom 'User' model that inherits from Django's 
    # built-in 'User' model and 'PermissionMixin'. To make it easy to include Django’s permission framework into 
    # your own user class, Django provides 'PermissionsMixin'. This is an abstract model you can include in the 
    # class hierarchy for your user model, giving you all the methods and database fields necessary to support 
    # Django’s permission model.
    def __str__(): # String representation of a User model instance
        return "@{}".format(self.username) # self.username attribute here comes from the built-in 'User'