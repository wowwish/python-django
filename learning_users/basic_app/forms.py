from django import forms
from django.contrib.auth.models import User # import the default built-in 'User' model from the Django admin app
from basic_app.models import UserProfileInfo

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta():
        model = User
        fields = ('username', 'email', 'password')

class UserProfileInfoForm(forms.ModelForm):
    class Meta():
        model = UserProfileInfo
        fields = ('portfolio_site', 'profile_pic') # included fields

# RUN: python manage.py migrate
# RUN: python manage.py makemigrations basic_app
# RUN: python manage.py migrate
