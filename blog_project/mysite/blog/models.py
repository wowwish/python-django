from django.db import models
from django.utils import timezone # For time and date utilities
from django.urls import reverse # To get URL string from a view and its parameters

# Create your models here.

class Post(models.Model):
    # Connect each author to an authorized user of the django admin page
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE) # Set up such that super-users with admin access can only author posts
    title = models.CharField(max_length=200)
    text = models.TextField()
    create_date = models.DateTimeField(default=timezone.now()) # Default creation date is obtained from 'timezone.now()'
    # This calls the current date of the timezone specified in the 'settings.py' file
    published_date = models.DateTimeField(blank=True, null=True) # This field can be left blank or empty or null. (For Draft Posts)
    def publish(self):
        self.published_date = timezone.now() # When published, save publication_date to current date and time in the App timezone
        self.save() # Save instance of this Model
    def approve_comment(self): # Method to return approved comments of the Post
        return self.comments.filter(approved_comment=True) # Return Filtered out comments
    def get_absolute_url(self): # Method to return user to a URL after successful completion of instantiation of an object/record of the Model
        return reverse("post_detail", kwargs={'pk': self.pk}) # After creating a post, go to the Post's detail (DetailView) page using its primary key 
        # (remove comments from Post that have their 'approved_comment' attribute set to 'False')
    def __str__(self): # String representation for an Instance of our Post model
        return self.title
    
class Comment(models.Model):
    post = models.ForeignKey('blog.Post', related_name='comments', on_delete=models.CASCADE) # Connect each Comment instance to an actual instance of model Post
    author = models.CharField(max_length=200) # Author of a comment may not be the same as author of a Post
    text = models.TextField()
    create_date = models.DateTimeField(default=timezone.now()) # Set default date-time to current date and time of the App timezone
    approved_comment = models.BooleanField(default=False) # All comments are unapproved by Default.
    def approve(self):
        self.approved_comment = True # Approve the comment
        self.save()
    def get_absolute_url(self):
        return reverse('post_list') # return user to the all posts list (ListView) after they comment on a post    
    def __str__(self): # String representation of an instance of Comment model
        return self.text


