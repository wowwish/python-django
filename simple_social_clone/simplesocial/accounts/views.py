# This views.py file is for the 'accounts' app
from django.shortcuts import render
from django.urls import reverse_lazy # Lazy version of 'reverse' that resolves view names, view references and URL parameters to URL strings
from . import forms # import forms from 'forms.py'
from django.views.generic import CreateView # in-built generic class-based view for model instance creation
# Create your views here.

class SignUp(CreateView):
    form_class = forms.UserCreateForm # Setup the form for the 'CreateView' class
    success_url = reverse_lazy('login') # Once someone has successfully signed up, and only when their data is
    # created and saved, redirect the user to the view named 'login'
    template_name = 'accounts/signup.html'
