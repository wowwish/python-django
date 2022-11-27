from django.shortcuts import render
from basicapp import forms

# Importing Forms defined in the 'forms.py' file of this application
# 'from . import forms' (or) 'from forms import FormName'

# Create your views here.

# Creating a view for an imported Form:
# def form_name_view(request):
#     form = forms.FormName()
#     return render(request, 'form_name.html', {'form': form})

def index(request):
    return render(request, 'basicapp/index.html')

def form_name_view(request):
    form = forms.FormName() # An empty instance of the form to be sent in the context dictionary
    # When someone submits the Form
    if request.method == 'POST':
        form = forms.FormName(request.POST)
        if form.is_valid(): # If the data entered in the Form is valid
            # DO SOMETHING
            print("VALIDATION SUCCESS.")
            # Get the Form data using respective class attributes of the Form
            print("NAME: ", form.cleaned_data['name'])
            print("EMAIL: ", form.cleaned_data['email'])
            print("TEXT: ", form.cleaned_data['text'])
    return render(request, 'basicapp/form_page.html', {'form': form})