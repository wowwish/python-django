from django.db import models
from django.urls import reverse # URL resolver
from django.conf import settings # Project Settings
from groups.models import Group
from django.contrib.auth import get_user_model # get the 'User' model that is currently active in this project
User = get_user_model() # Gets the currently active 'User' model from the 'accounts' app
import misaka # For markdown support in text content

# Create your models here.
class Post(models.Model):
    # REFER: https://docs.djangoproject.com/en/4.1/ref/models/fields/#foreignkey
    # REFER: https://docs.djangoproject.com/en/4.1/topics/db/queries/#related-objects
    # The 'Post' model class is related to the 'User' model class through a ForeignKey relationship that we are 
    # calling 'memberships'. The 'related_name' parameter allows us to access all the posts associated with 
    # a given user using 'user.posts'
    # When a User is deleted, the posts made by the user must also be deleted, hence, we follow the 'models.CASCADE'
    # deletion strategy here
    # REFER: https://docs.djangoproject.com/en/4.1/ref/models/fields/#django.db.models.ForeignKey.on_delete
    user = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True) # Set the 'created_at' automatically to the current date and time
    message = models.TextField()
    message_html = models.TextField(editable=False) # Field to hold the markdown styled message content
    # When a group is deleted, all post instances associated with that group should also be deleted. Hence, we
    # follow the 'models.CASCADE' deletion strategy here.
    # REFER: https://docs.djangoproject.com/en/4.1/ref/models/fields/#django.db.models.ForeignKey.on_delete
    group = models.ForeignKey(Group, related_name='Posts', null=True, blank=True, on_delete=models.CASCADE)
    def __str__(self): # method for string representation of instance of model
        return self.message
    def save(self, *args, **kwargs): # Method for preprocessing and saving the model data as an instance of the model
        self.message_html = misaka.html(self.message) # Convert the message text to markdown styled message
        super().save(*args, **kwargs) # Calling the 'save()' method from the parent model class 'model.Model'
    
    # REFER: https://docs.djangoproject.com/en/4.1/ref/models/instances/#get-absolute-url
    def get_absolute_url(self): # Method to define a URL for each model instance, with the help of the 
        # primary key of the 'User' model instance and the 'username' attribute of the model
        return reverse('posts:single', kwargs={'username': self.user.username, 'pk': self.pk})
    
    # Model metadata is “anything that’s not a field”, such as ordering options (ordering), database table name 
    # (db_table), or human-readable singular and plural names ('verbose_name' and 'verbose_name_plural'). 
    # None are required, and adding class 'Meta' to a model is completely optional.
    class Meta: # REFER: https://docs.djangoproject.com/en/4.1/topics/db/models/#meta-options
        ordering = ['-created_at'] # # Order the instances of the Model according to their 
        # 'created_at' datetime attribute when obtaining a list of Model objects, with the mose recent posts
        # at the top (Descending order due to negative sign)
        unique_together = ['user', 'message'] # set of field names whose values must be unique when considered together 
        # for an instance of the model (Composite key for the model instance)
