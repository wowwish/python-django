from django.db import models
from django.urls import reverse

# Create your models here.
# When you do not set a Primary key for your Model, Django sets an in-built serial number for the records of the Model
# and uses that as the Primary Key for the Model. This Default Primary Key can be accessed using the '.id' field name.

class School(models.Model):
    name = models.CharField(max_length=256)
    principal = models.CharField(max_length=256)
    location = models.CharField(max_length=256)
    # Creating string representation of Model
    def __str__(self):
        return self.name
    # A method to return URL for redirection of the user upon creating an instance of this Model using a 
    # Class Based View such as CreateView.
    # To callers, this method should appear to return a string that can be used to refer to the object over HTTP.
    def get_absolute_url(self):
        return reverse("basic_app:detail", kwargs={'pk': self.pk}) # Redirect the user to a url that renders
        # the 'basic_app:detail" page with the 'pk' argument for the view as 'self.pk' (redirect the user to
        # the detail page of the same School instance that they created). 
        # Define a 'get_absolute_url()' method to tell Django how to calculate the canonical URL for an object. 
    
    
class Students(models.Model):
    name = models.CharField(max_length=256)
    age = models.PositiveIntegerField()
    # A Foreign key from the 'School' Model for each 'Students' record.
    # ForeignKey.related_name: The name to use for the relation from the related object back to this one. 
    # It’s also the default value for related_query_name (the name to use for the reverse filter name from 
    # the target model). 
    # If a model has a ForeignKey, instances of the foreign-key model will have access to a 'Manager' that returns 
    # all instances of the first model. By default, this 'Manager' is named 'FOO_set', where 'FOO' is the source 
    # model name, lowercased. This 'Manager' returns 'QuerySets', which can be filtered and manipulated.
    # You can override the 'FOO_set' name by setting the 'related_name' parameter in the ForeignKey definition.
    # Here, 'school.students.all()' will return a 'QuerySet' of all 'Students' objects related to 'School'
    school = models.ForeignKey(School, related_name='students', on_delete=models.CASCADE)