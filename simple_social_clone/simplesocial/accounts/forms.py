from django.contrib.auth import get_user_model # Get the currently active user model for this project. 
# This method will return the currently active user model – the custom user model if one is specified, or 
# the built-in 'User' model from 'django.contrib.auth' otherwise.
# REFER: https://docs.djangoproject.com/en/4.1/topics/auth/customizing/#referencing-the-user-model
from django.contrib.auth.forms import UserCreationForm # Built-in user creation form from Django


class UserCreateForm(UserCreationForm): # Custom user-creation form that inherits from the in-built 'UserCreationForm'
    class Meta: # The Meta class that is mandatory for every Django form class
        fields = ('username', 'email', 'password1', 'password2') # Fields included from the model into the form
        model = get_user_model() # gets the current active model for user instances
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) # Initiate the 'UserCreationForm' class with the passed arguments
        self.fields['username'].label = 'Display Name' # Set the label for the 'username' field in the template form to 'Display Name'
        self.fields['email'].label = 'Email Address' # Set the label for the 'email' field in the template form to 'Email Address'
