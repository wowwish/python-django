from django.contrib import admin
from . import models

# Reorder the fields shown in the Detail View of a Model instance in the Admin Page
# Create a Field customizaton class for the Model Instance by inheriting from the 'admin.ModelAdmin' parent class
class MovieAdmin(admin.ModelAdmin): # The name of this customization class should be '<Model_name>Admin'
    # actual fields of the 'Model' in the order you want to view them in the instance Detail View in Admin Page
    fields = ['release_year', 'title', 'length'] 
    
    # List of fields that you want to have a search box to search through field values in the Admin Page List View of the Model
    search_fields = ['title', 'length']
    
    # Add search filters for your model fields in the Admin Page List View of your Custom Models
    list_filter = ['release_year', 'length', 'title'] # Adds value based filters for all fields of the Movie model
    # in the List View of the 'Movie' model in the Admin Page

    # The list of fields to be displayed (for each instance of the model) in the List View of the 'Movie' model Admin Page
    list_display = ['title', 'release_year', 'length'] # The order here is the order in which the fields are shown
    # This overrides the __str__() method's string which is usually displayed in the List View of the model in the Admin Page.
    # Here, we are displaying all fields of the model in the List View at the Admin Page.
    # The first field is clickable and takes you to the Detail View of a particular instance of the Model from its List View
    # The Headers of the other fields can be used for Sorting the List View.

    # You can also add the ability to edit the attribute/field values of field from the List View of Models in the 
    # Admin Page iteslf, instead of going to the Detail View Page of a particular instance to perform the edit
    list_editable = ['length'] # List of attributes/fields that are made editable from the List View of Admin Page
    # KEEP IN MIND THAT THE FIELD HAS TO BE FIRST DISPLAYED IN THE LIST VIEW USING 'list_display' ATTRIBUTE 
    # FOR IT TO BE EDITABLE FROM THE LIST VIEW

    


# Register your models here.
admin.site.register(models.Customer)
admin.site.register(models.Movie,MovieAdmin) # Register the Admin Page Customization class as well along 
# with the Model For the Admin Page View of the Model