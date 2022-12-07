from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from basic_app.forms import UserForm, UserProfileInfoForm

# Imports for User Logins

# Use 'authenticate()' to verify a set of credentials. It takes credentials as keyword arguments, 
# (username and password for the default case), checks them against each authentication backend, and returns 
# a User object if the credentials are valid for a backend. If the credentials aren’t valid for any backend 
# or if a backend raises PermissionDenied, it returns 'None'.

# To log a user in, from a view, use 'login()'. It takes an HttpRequest object and a built-in Django 'User' object. 
# 'login()' saves the user’s ID in the session, using Django’s session framework.

# To log out a user who has been logged in via 'django.contrib.auth.login()', use 'django.contrib.auth.logout()' 
# within your view. It takes an HttpRequest object and has no return value. 
# When you call 'logout()', the session data for the current request is completely cleaned out. 
# All existing data is removed. This is to prevent another person from using the same web browser to log in and 
# have access to the previous user’s session data. If you want to put anything into the session that will be 
# available to the user immediately after logging out, do that after calling 'django.contrib.auth.logout()'.

from django.contrib.auth import authenticate, login, logout
# 'HttpResponseRedirect()' takes a single argument: the URL to which the user will be redirected. 
# You should always return an 'HttpResponseRedirect()' after successfully dealing with POST data
from django.http import HttpResponseRedirect, HttpResponse
# We are using the 'reverse()' function in the 'HttpResponseRedirect()' constructor in this example. 
# This function helps avoid having to hardcode a URL in the view function. It is given the name of the view that 
# we want to pass control to and the variable portion of the URL pattern that points to that view.
from django.urls import reverse
from django.contrib.auth.decorators import login_required # wrap views with this decorator to make the view 
# accessible only to logged in users


# Create your views here.

def index(request):
    return render(request, 'basic_app/index.html')

@login_required # Only allow Logged-in Users to Log-out
def user_logout(request): # User logout page
    logout(request) # Logout the user using the built-in 'logout()' function
    # 'reverse()' returns an absolute path reference (a URL without the domain name) matching a given view and 
    # optional parameters. Any special characters in the resulting path will be encoded with the corresponding value.
    # This is a way to output links without violating the DRY principle by having to hard-code URLs in your templates.
    # The 'reverse()' function can reverse a large variety of regular expression patterns for URLs, but not 
    # every possible one. The main restriction at the moment is that the pattern cannot contain alternative 
    # choices using the vertical bar ("|") character.
    return HttpResponseRedirect(reverse('index')) # Redirect to the index page after Logout

# View for some special Page that requires Log-in
@login_required
def special(request):
    return HttpResponse("YOU ARE LOGGED IN. NICE!")

def register(request):
    registered = False # Assume that the Form data (user) is not already registered
    if request.method == 'POST':
        user_form = UserForm(data = request.POST)
        profile_form = UserProfileInfoForm(data = request.POST)
        if user_form.is_valid() and profile_form.is_valid(): # If both forms have valid data
            user = user_form.save() # Save User information directly to the database
            user.set_password(user.password) # Hashes the password according to the Hashing Method order in the 'settings.py' file
            # This is an in-built method of the in-built User model class. It only sets the User's password to the hashed
            # form of the given string 'user.password'.
            user.save() # Save the User information. This is where all user information including the password is saved.
            # REMEMBER: You can use 'commit=False' in the '.save()' method of a ModelForm to manipulate the Form Data before
            # saving it as a Model instance. This will also prevent collision errors from saving the same Form data twice!
            profile = profile_form.save(commit=False)
            profile.user = user # Linking up the one-to-one relationship as defined in the 'models.py' file between the 
            # 'User' model instance and the corresponding 'UserProfileInfo' model instance.
            if 'profile_pic' in request.FILES: # 'request.FILES' is a dictionary with all the Files uploaded in the Form
                # We use the key defined in the Model to access the File from the 'request.FILES' dictionary
                profile.profile_pic = request.FILES['profile_pic']
            profile.save() # Actual saving of Profile information to the Model
            registered = True # Set the User Registered flag to True if both forms are valid and saving their info is successful
        else: # When any of the two Forms have Invalid Data
            print(user_form.errors, profile_form.errors) # Print out the Form Validation Errors
    else: # If request.method is not POST
        user_form = UserForm()
        profile_form = UserProfileInfoForm()
    return render(request, 'basic_app/registration.html', 
                        {'user_form': user_form, 'profile_form': profile_form, 'registered': registered, })

# For Login / Logout:
# Set up the login views
# use built-in decorators for access to views only when user is logged in
# add the LOGIN_URL in settings.py file
# create the login.html template
# edit the urls.py file                        


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username') # Get the value of the field named 'username' from the data submitted
        # through the login form ('name' attribute is 'username' for the input field)
        password = request.POST.get('password') # Get the value of the 'password' field from the data submitted
        # through the login form ('name' attribute is 'password' for the input field)
        user = authenticate(username=username, password=password) # A user object is returned by authenticate()
        if user: # If user is authenticated
            if user.is_active: # If the user is an Active user
                login(request, user) # Login the user using Django's built-in function 'login'
                return HttpResponseRedirect(reverse('index')) # If user login is successful and the user is
                # an active user, redirect the user to the homepage 'index.html'
            else: # If the user account is not active
                return HttpResponse("ACCOUNT NOT ACTIVE!")
        else: # If user is not authenticated (malicious login), print the username and password to console.
            print("Someone tried to login and failed!")
            print("Username: {} and password {}".format(username, password)) # Error Logging
            return HttpResponse('INVALID LOGIN DETAILS SUPPLIED!')
    else: # If the request method is not POST
        return render(request, 'basic_app/login.html', context={})

