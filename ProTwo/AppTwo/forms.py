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
# THE MODEL HAS TO BEE MIGRATED FOR MODELFORM CLASS TO WORK PROPERLY AND SAVE CONTENT FROM THE FORM AS A MODEL INSTANCE

from django import forms
from AppTwo.models import User

# Creating the form class
class NewUserForm(forms.ModelForm):
    # DEFINE FIELDS HERE
    class Meta:
        model = User
        fields = '__all__'


