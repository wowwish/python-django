from django.shortcuts import render
from django.http import HttpResponse
from AppTwo.models import User
from AppTwo.forms import NewUserForm # A model form

# Create your views here.

def index(request):
    return HttpResponse('<em>My Second App</em>')

def help(request):
    return render(request, 'AppTwo/help.html', context={'insert_me': 'Help Page'})

def table(request):
    return render(request, 'AppTwo/list_users.html', context={'user_list': User.objects.order_by('first_name') })

def new(request):
    # converting form data into the corresponding model for a ModelForm
    form = NewUserForm() # An empty instance of the form to be sent in the context dictionary
    # When someone submits the Form
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid(): # If the data entered in the Form is valid
            form.save(commit=True) # Save the form data as an instance of the corresponding Model of the Form
            return help(request) # Return the user back to the home page upon successful creation of Model instance
        else:
            print('ERROR FORM INVALID')

    return render(request, 'AppTwo/new_user.html', {'form': form})
    # The page to be renered for the first time when this view is used or when there is 
    # no POST request submitted.