# https://docs.djangoproject.com/en/4.1/ref/forms/validation/

# DJANGO FORMS ADVANTAGES:
# Quickly generate HTML form widgets
# Validate data and process it into a python data structure
# Create form versions of our Models, quickly update models from Forms

# STEPS:
# Create a 'forms.py' file inside the application, just like this one
# Call Django's built-in Form Classes within this file

# from django import forms

# class FormName(forms.Form):
#     name = forms.CharField()
#     email = forms.CharField()
#     text = forms.CharField(widget=forms.Textarea)

# Inside your 'views.py' file, import the Forms defined here. You can create a new view for the form in the
# 'views.py' file of your application

# Then, we add the view to the 'urls.py' file of the application/project.

# We can then create the templates folder along with the HTML file that will hold the template tagging for that form
# Remember to update the 'settings.py' file to reflect the TEMPLATE_DIR variable!
# Also remember that your views should reflect sub-directories inside templates folder.

# Now you can go to the 'form_name.html' file in your templates folder and add the template tagging that will create
# the Django form. There are several ways to "inject" the Form into the template using template tagging. You
# can just pass in the key from the context dictionary like so: {{ form }}
# The Form Data can be moved around using GET and POST requests via the HTTP protocol.

# SAMPLE FORM TEMPLATE TAGGING:
# <div class = "container">
#     <form method="POST">
#         {{ form.as_p }} <!-- Puts the form elements inside a paragraph tag for nice formatting. Check django docs for other ways of including forms for example in a table-->
#         {% csrf_token %} <!-- cross-site request forgery token to secure HTTP POST requests from Form -->
#         <input type="submit" class="btn btn-primary" value="Submit">
#     </form>
# </div>

# The Django Framework actually requires the CSRF token and your Form may not work without it, especially when
# it uses POST. It works by using a "hidden input" which is a random code and checking that it matches the user's
# local site page. THIS CSRF TOKEN PREVENTS USERS FROM SUBMITTING THE FORM DATA TO ANY OTHER WEBSITE.

# We need to inform the view that if we get a POST back, we should check if the data is valid and if so, grab the data.
# Upon recieving a validated form, we can access a dictionary-like attribute of the "cleaned_data"

# def form_name_view(request):
    # form = forms.FormName()
    # Check to see if we get a POST back
    # if request.method == 'POST':
        # In which case we pass in that request
        # form = forms.FormName(request.POST)
        # Check to see form is valid
        # if form.is_valid():
            # Do something
    #         print("Form Validation Success. Prints in console.")
    #         print("Name"+form.cleaned_data["name"])
    #         print("Email"+form.cleaned_data["email"])
    #         print("Text"+form.cleaned_data["text"])
    # return render(request, 'basicapp/form_page.html', {'form': form})


from django import forms
from django.core import validators # built-in form validators

# creating custom validator functions can also be used with Django's build-in validaton framework
def check_for_z(value):
    if value[0].lower() != 'z':
        raise forms.ValidationError("name needs to start with z")

class FormName(forms.Form):
    # Class attributes
    name = forms.CharField(validators=[check_for_z]) # using custom validation function with Django's validation framework
    email = forms.EmailField()
    verify_email = forms.EmailField(label='Enter your email again:')
    text = forms.CharField(widget=forms.Textarea)
    # Hidden Form field for catching malicious bots - default/normal way
    # botcatcher = forms.CharField(required=False, widget=forms.HiddenInput) 
    # Hidden Form field for catching malicious bots - using built-in validators of Django
    botcatcher = forms.CharField(required=False, 
                                 widget=forms.HiddenInput,
                                 validators=[validators.MaxLengthValidator(0)])
    # Default Custom Validator Method. Django automatically looks for 'clean_*' methods inside the form class
    # and uses them for Validating the form
    # def clean_botcatcher(self):
    #     botcatcher = self.cleaned_data["botcatcher"]
    #     if (len(botcatcher) > 0): # Some robot has scraped the page and added this hidden input
    #         raise forms.ValidationError("GOTCHA BOT!")
    #     return botcatcher
    def clean(self): # A single clean method for the entire form data at once
        all_clean_data = super().clean()
        email = all_clean_data['email']
        vmail = all_clean_data['verify_email']
        if email != vmail:
            raise forms.ValidationError("make sure emails match!")

# Django has built-in validators you can conveniently use to validate your Forms (or check for bots!)
# Validations: Adding a check for empty fields, adding a check for a "bot", adding a 'clean' method for the entire form


# CONNECTING MODELS WITH FORMS IN DJANGO
# The 'forms.ModelForms' helper class from Django allows us to create a form from a pre-existing model. We then
# add an inline class (class within class) 'Meta' that provides information on connecting the Model to the Form.

# from django import forms
# from myapp.models import MyModel
# class MyNewForm(forms.ModelForm):
#     # Form Fields go here with validator params
#     class Meta:
#         model = MyModel
#         fields = "__all__" # Grab all the fields of the model and place them into the Form 
#         exclude = ['field1', 'field2'] # fields of the Model to exclude in the Form
#         fields = ('field1', 'field2') # fields of the Model included in the Form

# REFER: https://docs.djangoproject.com/en/4.1/topics/forms/modelforms/
# Briefly, the steps to use ModelForms are:
# Create a ModelForm in this 'forms.py' file
# Connect the form in the template
# Edit 'views.py' to show the form
# Figure out how to '.save()' the form data into model
# Verify that the model is admin registered.

