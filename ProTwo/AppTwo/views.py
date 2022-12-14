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
            # Every ModelForm also has a 'save()' method. This method creates and saves a database object from the data 
            # bound to the form. A subclass of ModelForm can accept an existing model instance as the keyword argument 
            # instance; if this is supplied, 'save()' will update that instance. If it’s not supplied, 'save()' will create 
            # a new instance of the specified model. 
            # Note that if the form hasn’t been validated, calling save() will do so by checking form.errors. 
            # A ValueError will be raised if the data in the form doesn’t validate – i.e., if form.errors evaluates to True.
            # If an optional field doesn’t appear in the form’s data, the resulting model instance uses the model 
            # field default, if there is one, for that field.
            # This save() method accepts an optional commit keyword argument, which accepts either True or False. 
            # If you call save() with commit=False, then it will return an object that hasn’t yet been saved to the 
            # database. In this case, it’s up to you to call save() on the resulting model instance. This is useful if 
            # you want to do custom processing on the object before saving it, or if you want to use one of the specialized 
            # model saving options. commit is True by default.
            # REFER: https://docs.djangoproject.com/en/4.1/topics/forms/modelforms/#the-save-method
            form.save(commit=True) # Save the form data as an instance of the corresponding Model of the Form
            return help(request) # Return the user back to the home page upon successful creation of Model instance
        else:
            print('ERROR FORM INVALID')

    return render(request, 'AppTwo/new_user.html', {'form': form})
    # The page to be renered for the first time when this view is used or when there is 
    # no POST request submitted.