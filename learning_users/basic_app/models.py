from django.db import models
from django.contrib.auth.models import User


# Previously, when we've logged into the Admin page, we have seen that there is already a built-in Authorization
# and Authentication model set in place called 'Users'. That User object has a few key features:
# Username, Email, Password, First Name and Surname
# There are also some other attributes of the User object, such as 'is_active', 'is_staff', 'is_superuser'
# You might want to add more features to this User object such as links and Profile Pictures. You can do this
# by creating another Class that has a relationship to the User class in this 'models.py' file like so:

# class UserProfileInfo(models.Model):
#     # Create Relationship (don't inherit from User - The default built-in model of the Django 'admin' app!)
#     user = models.OneToOneField(User)
#     # Add any additional attributes you want
#     portfolio = models.URLField(blank=True)
#     picture = models.ImageField(upload_to='profile_pics') # Install the 'pillow' python package to work with images and store in this field
#     def __str__(self):
#         # Built-in attribute of 'django.contrib.auth.models.User' !
#         return self.user.username

# Then register the model in 'admin.py' using 'admin.site.register(UserProfileInfo)'
# User uploaded content will go to the media folder in MEDIA_ROOT from 'settings.py'
# Next, implement the Django form in 'forms.py' that the User can use to work with the website.
# Like this:

# from django import forms
# from basic_app.models import UserProfileInfo

# class UserProfileInfoForm(forms.ModelForm):
#     portfolio = forms.URLField(required=True)
#     picture = forms.ImageField(required=False)
#     class Meta():
#         model = UserProfileInfo
#         exclude = ('user',) # Fields excluded from the model

# Create your models here.

class UserProfileInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # additional
    portfolio_site = models.URLField(blank=True) # Optional field since 'blank=True'
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True) # create subdirectory 'profile_pics' in 'media' folder of the project
    def __str__(self):
        return self.user.username # returns the 'username' attribute of the default 'User' model built-in into Django admin app

# RUN: python manage.py migrate
# RUN: python manage.py makemigrations basic_app
# RUN: python manage.py migrate