from django.db import models
from django.urls import reverse # URL resolver to build a URL
from django.utils.text import slugify
# 'django.utils.text.slugify' converts a string to a URL slug by:
#   *  Converting to ASCII if allow_unicode is False (the default).
#   *  Converting to lowercase.
#   *  Removing characters that aren’t alphanumerics, underscores, hyphens, or whitespace.
#   *  Replacing any whitespace or repeated dashes with single dashes.
#   *  Removing leading and trailing whitespace, dashes, and underscores.
# We use the 'misaka' library for external link embedding ajd markdown support in Posts. (pip install misaka)
import misaka
from django.contrib.auth import get_user_model # get the 'User' model that is currently active in this project
User = get_user_model() # Gets the currently active 'User' model from the 'accounts' app
# For usage of custom template tags
# We use it here for grabbing the content from the context dictionary in templates using the model's 'related_name' ForeignKey parameter
# REFER: https://docs.djangoproject.com/en/4.1/howto/custom-template-tags/#how-to-create-custom-template-tags-and-filters
from django import template 
register = template.library 

# Create your models here.
class Group(models.Model):
    name = models.CharField(max_length=255, unique=True) # unique group names
    # A slug representation of the 'Group' instance name
    slug = models.SlugField(allow_unicode=True, unique=True) # Group slug for creating URL for groups
    description = models.TextField(blank=True,default='')
    description_html = models.TextField(editable=False, default='', blank=True)
    # REFER: https://docs.djangoproject.com/en/4.1/ref/models/fields/#manytomanyfield
    members = models.ManyToManyField(User, through='GroupMembers') # The Many-Groups-to-Many-Users relationship
    # is modelled through the instances of the 'GroupMMember' model. Django will automatically generate a table 
    # to manage many-to-many relationships. However, if you want to manually specify the intermediary table, 
    # you can use the 'through' option to specify the Django model that represents the intermediate table that 
    # you want to use.
    def __str__(self): # String representation of a 'Group' object
        return self.name
    # REFER: https://docs.djangoproject.com/en/4.1/ref/models/instances/#django.db.models.Model.save
    def save(self, *args, **kwargs): # Method to pre-process and save each instance of the model
        self.slug = slugify(self.name) # Slugify the name and store it as the slug attribute of the model instance
        self.description_html = misaka.html(self.description) # To render markdown in HTML
        super().save(*args, **kwargs) # calling the 'save()' method of the parent class as well (models.Model) 
        # with auxilliary arguments
    # REFER: https://docs.djangoproject.com/en/4.1/ref/models/instances/#get-absolute-url
    def get_absolute_url(self): # Method to tell Django how to calculate the canonical URL for the object/model instance
        return reverse('groups:single', kwargs={'slug': self.slug}) # resolve URL string for the model instance 
        # using the 'self.slug' attribute in the URL

    # Model metadata is “anything that’s not a field”, such as ordering options (ordering), database table name 
    # (db_table), or human-readable singular and plural names ('verbose_name' and 'verbose_name_plural'). 
    # None are required, and adding class 'Meta' to a model is completely optional.
    class Meta: # REFER: https://docs.djangoproject.com/en/4.1/topics/db/models/#meta-options
        ordering = ['name'] # Order the instances of the Model according to their 'name' attribute when obtaining a list of Model objects

# Model to store 
class GroupMembers(models.Model):
    # The 'GroupMembers' class is related to the 'Group' class through a ForeignKey relationship that we are calling 'memberships'
    # The 'related_name' parameter allows us to access all the memberships associated with a given group 
    # using 'group.memberships'
    # REFER: https://docs.djangoproject.com/en/4.1/ref/models/fields/#foreignkey
    # REFER: https://docs.djangoproject.com/en/4.1/topics/db/queries/#related-objects
    # When a group is deleted, the Group Membership should also be deleted, hence we use 'models.CASCADE' 
    # as the deletion strategy here
    # REFER: https://docs.djangoproject.com/en/4.1/ref/models/fields/#django.db.models.ForeignKey.on_delete
    group = models.ForeignKey(Group, related_name='memberships', on_delete=models.CASCADE)
    # The 'User' model returned by 'get_current_user()' is related to the 'GroupMembers' class through a ForeignKey
    # relationship that we are calling 'user_groups'
    # The 'related_name' parameter allows us to access all the group memberships associated with a given user 
    # using 'user.user_groups'
    # REFER: https://docs.djangoproject.com/en/4.1/ref/models/fields/#foreignkey
    # REFER: https://docs.djangoproject.com/en/4.1/topics/db/queries/#related-objects
    # When a user is deleted, the Group Membership instances of that user should also be deleted, hence, we follow
    # the 'models.CASCADE' deletion strategy here
    # REFER: https://docs.djangoproject.com/en/4.1/ref/models/fields/#django.db.models.ForeignKey.on_delete
    user = models.ForeignKey(User, related_name='user_groups', on_delete=models.CASCADE)
    def __str__(self): # String representation for the Model instance
        return self.user.username # User the 'username' from the 'User' model instance associated with each 'GroupMembers' instance
    # for its string representation in the admin page list-view
    # Model metadata is “anything that’s not a field”, such as ordering options (ordering), database table name 
    # (db_table), or human-readable singular and plural names ('verbose_name' and 'verbose_name_plural'). 
    # None are required, and adding class 'Meta' to a model is completely optional.
    class Meta:
        # REFER: https://docs.djangoproject.com/en/4.1/ref/models/options/#unique-together
        unique_together = ('group', 'user') # set of field names whose values must be unique when considered together 
        # for an instance of the model (Composite key for the model instance)